from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Actuator

actuators_bp = Blueprint('actuators', __name__, template_folder='templates')

@actuators_bp.route('/')
def list_actuators():
    actuators = Actuator.query.all()
    return render_template('actuators.html', actuators=actuators)

@actuators_bp.route('/register', methods=['GET','POST'])
def register_actuator():
    if request.method == 'POST':
        db.session.add(Actuator(name=request.form['actuator']))
        db.session.commit()
        return redirect(url_for('actuators.list_actuators'))
    return render_template('register_actuator.html')

@actuators_bp.route('/delete', methods=['GET','POST'])
def delete_actuator():
    if request.method == 'POST':
        aid = request.form['actuator_id']
        Actuator.query.filter_by(id=aid).delete()
        db.session.commit()
        return redirect(url_for('actuators.list_actuators'))
    actuators = Actuator.query.all()
    return render_template('remove_actuator.html', actuators=actuators)
