from flask import Flask, render_template, jsonify
from flask_mqtt import Mqtt
import config
from extensions import db

from blueprints.auth      import auth_bp
from blueprints.sensors   import sensors_bp
from blueprints.actuators import actuators_bp
from blueprints.dashboard import dashboard_bp

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(config)

db.init_app(app)
mqtt_client = Mqtt(app)

sensor_data = {'dht': None, 'mq2': None}

app.register_blueprint(auth_bp)
app.register_blueprint(sensors_bp,   url_prefix='/sensors')
app.register_blueprint(actuators_bp, url_prefix='/actuators')
app.register_blueprint(dashboard_bp)

from models import Sensor, SensorReading

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT connected, subscribing to sensors…")
        mqtt_client.subscribe(config.TOPIC_SENSOR_DHT)
        mqtt_client.subscribe(config.TOPIC_SENSOR_MQ2)
    else:
        print("MQTT connect failed:", rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, msg):
    topic   = msg.topic
    payload = msg.payload.decode()
    from app import app as _app
    with _app.app_context():
        if topic == config.TOPIC_SENSOR_DHT:
            sensor_data['dht'] = payload
            s = Sensor.query.filter_by(name='dht').first()
            if s:
                db.session.add(SensorReading(sensor_id=s.id, value=payload))
                db.session.commit()
        elif topic == config.TOPIC_SENSOR_MQ2:
            sensor_data['mq2'] = payload
            s = Sensor.query.filter_by(name='mq2').first()
            if s:
                db.session.add(SensorReading(sensor_id=s.id, value=payload))
                db.session.commit()

@app.route('/api/sensors')
def api_sensors():
    return jsonify(sensor_data)

@app.route('/history/sensors')
def history_sensors():
    readings = (SensorReading.query
                .join(Sensor)
                .order_by(SensorReading.timestamp.desc())
                .limit(100)
                .all())
    return render_template('history_sensors.html', readings=readings)

@app.route('/history/actuators')
def history_actuators():
    from models import ActuatorCommand
    commands = (ActuatorCommand.query
                .join(Actuator)
                .order_by(ActuatorCommand.timestamp.desc())
                .limit(100)
                .all())
    return render_template('history_actuators.html', commands=commands)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from models import Sensor, Actuator, User
        from werkzeug.security import generate_password_hash
        if not Sensor.query.first():
            db.session.add_all([Sensor(name='dht'), Sensor(name='mq2')])
        if not Actuator.query.first():
            db.session.add_all([Actuator(name='servo'), Actuator(name='buzzer')])
        if not User.query.first():
            db.session.add_all([
                User(username='admin', password=generate_password_hash('admin123')),
                User(username='user1', password=generate_password_hash('pass1'))
            ])
        db.session.commit()
    app.run(host='0.0.0.0', port=8080, debug=True)
