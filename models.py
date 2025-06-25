from datetime import datetime
from extensions import db

class User(db.Model):
    id           = db.Column(db.Integer,   primary_key=True)
    username     = db.Column(db.String(80), unique=True, nullable=False)
    password     = db.Column(db.String(128), nullable=False)

class Sensor(db.Model):
    id       = db.Column(db.Integer,   primary_key=True)
    name     = db.Column(db.String(80), unique=True, nullable=False)
    readings = db.relationship('SensorReading', back_populates='sensor')

class SensorReading(db.Model):
    id         = db.Column(db.Integer,       primary_key=True)
    sensor_id  = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    timestamp  = db.Column(db.DateTime,      default=datetime.utcnow, nullable=False)
    value      = db.Column(db.String(80),    nullable=False)
    sensor     = db.relationship('Sensor', back_populates='readings')

class Actuator(db.Model):
    id        = db.Column(db.Integer,   primary_key=True)
    name      = db.Column(db.String(80), unique=True, nullable=False)
    commands  = db.relationship('ActuatorCommand', back_populates='actuator')

class ActuatorCommand(db.Model):
    id          = db.Column(db.Integer,     primary_key=True)
    actuator_id = db.Column(db.Integer, db.ForeignKey('actuator.id'), nullable=False)
    timestamp   = db.Column(db.DateTime,    default=datetime.utcnow, nullable=False)
    command     = db.Column(db.String(200), nullable=False)
    actuator    = db.relationship('Actuator', back_populates='commands')
