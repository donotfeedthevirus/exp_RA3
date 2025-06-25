from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/')
def login():
    return render_template('login.html')

@auth_bp.route('/validated_user', methods=['POST'])
def validated_user():
    user = request.form['user']
    pwd  = request.form['password']
    u = User.query.filter_by(username=user).first()
    if u and check_password_hash(u.password, pwd):
        return redirect(url_for('dashboard.home'))
    return '<h1>Invalid credentials</h1>', 401

@auth_bp.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@auth_bp.route('/users/register', methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['user']
        pwd_hash = generate_password_hash(request.form['password'])
        db.session.add(User(username=username, password=pwd_hash))
        db.session.commit()
        return redirect(url_for('auth.list_users'))
    return render_template('register_user.html')

@auth_bp.route('/users/delete', methods=['GET','POST'])
def delete_user():
    if request.method == 'POST':
        uid = request.form['user_id']
        User.query.filter_by(id=uid).delete()
        db.session.commit()
        return redirect(url_for('auth.list_users'))
    users = User.query.all()
    return render_template('remove_user.html', users=users)
