from app import app, db
from app.users.model import User
from flask import jsonify, request
from datetime import datetime
from hashlib import sha256

prefix = '/api/users'


@app.route(prefix + '', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if users:
        users_list = [user.to_dict() for user in users]
        return jsonify(users_list)
    else:
        return jsonify([])


@app.route(prefix + '/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user:
        user_dict = user.to_dict()
        return jsonify(user_dict)
    else:
        return jsonify({})


@app.route('/api/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')
    can_create_users = request.json.get('can_create_users')
    registered_at = datetime.now()
    password_hash = sha256(password.encode('utf-8')).hexdigest()
    print(password_hash)
    user = User(username=username, first_name=first_name, last_name=last_name, email=email,
                registered_at=registered_at, can_create_users=can_create_users, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return {'status': 'success'}


@app.route('/api/users/<user_id>', methods=['PUT'])
def edit_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    if request.form.get('username'):
        user.username = request.json.get('username')
    if request.form.get('first_name'):
        user.first_name = request.json.get('first_name')
    if request.form.get('last_name'):
        user.last_name = request.json.get('last_name')
    if request.form.get('can_create_users'):
        user.status = request.json.get('can_create_users')
    db.session.commit()
    return {'status': 'success'}