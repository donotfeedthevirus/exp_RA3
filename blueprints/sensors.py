from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Sensor

sensors_bp = Blueprint('sensors', __name__, template_folder='templates')

@sensors_bp.route('/')
def list_sensors():
    sensors = Sensor.query.all()
    return render_template('sensors.html', sensors=sensors)

@sensors_bp.route('/register', methods=['GET','POST'])
def register_sensor():
    if request.method == 'POST':
        db.session.add(Sensor(name=request.form['sensor']))
        db.session.commit()
        return redirect(url_for('sensors.list_sensors'))
    return render_template('register_sensor.html')

@sensors_bp.route('/delete', methods=['GET','POST'])
def delete_sensor():
    if request.method == 'POST':
        sid = request.form['sensor_id']
        Sensor.query.filter_by(id=sid).delete()
        db.session.commit()
        return redirect(url_for('sensors.list_sensors'))
    sensors = Sensor.query.all()
    return render_template('remove_sensor.html', sensors=sensors)
