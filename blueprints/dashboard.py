from flask import Blueprint, render_template, request, jsonify
import config, json

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/home')
def home():
    return render_template('home.html')

@dashboard_bp.route('/realtime')
def realtime():
    return render_template('realtime.html')

@dashboard_bp.route('/control')
def control():
    return render_template('control.html')

@dashboard_bp.route('/api/servo', methods=['POST'])
def servo_control():
    from app import mqtt_client
    from extensions import db
    from models import Actuator, ActuatorCommand
    data = request.get_json()
    angle = data.get('angle')
    mqtt_client.publish(config.TOPIC_ACTUATOR_SERVO, str(angle))
    act = Actuator.query.filter_by(name='servo').first()
    cmd = ActuatorCommand(actuator_id=act.id, command=json.dumps({'angle': angle}))
    db.session.add(cmd)
    db.session.commit()
    return jsonify({'status': 'ok', 'angle': angle})

@dashboard_bp.route('/api/buzzer', methods=['POST'])
def buzzer_control():
    from app import mqtt_client
    from extensions import db
    from models import Actuator, ActuatorCommand
    data = request.get_json()
    freq = data.get('frequency')
    vol  = data.get('volume')
    payload = json.dumps({'frequency': freq, 'volume': vol})
    mqtt_client.publish(config.TOPIC_ACTUATOR_BUZZER, payload)
    act = Actuator.query.filter_by(name='buzzer').first()
    cmd = ActuatorCommand(actuator_id=act.id, command=payload)
    db.session.add(cmd)
    db.session.commit()
    return jsonify({'status': 'ok', 'payload': payload})
