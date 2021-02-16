from flask import request

from app import app, db
import app.auth.service as s


@app.route('/api/auth/check', methods=['POST'])
def check_login_status():
    print('Checking login status')
    return s.check_login_status()


@app.route('/api/auth/refresh', methods=['POST'])
def refresh_access_token():
    print('Refreshing access token')
    refresh_token = request.cookies.get('refreshToken')
    user_agent = request.user_agent.string
    return s.refresh_access_token(refresh_token, user_agent)


@app.route('/api/auth/login', methods=['POST'])
def login():
    print('Logging in')
    data = request.json
    email = data['email']
    password = data['password']
    return s.login(email, password)


@app.route('/api/auth/register', methods=['POST'])
def register():
    print('Registering')
    data = request.json
    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']
    status = data['status']
    return s.register(username, first_name, last_name, email, password, status)


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    print('Logging out')
    return s.logout()


@app.route('/api/auth/profile', methods=['POST'])
def get_current_user():
    print('Getting current user\'s info')
    return s.get_current_user_profile()
