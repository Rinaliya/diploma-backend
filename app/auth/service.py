import hashlib
from flask import request, make_response, jsonify
from app import User, db
from app.auth.tokens_utils import encode_auth_token, decode_auth_token, check_blacklist
from app.auth.blacklist_token_model import BlacklistToken
from app.auth.refresh_token_model import RefreshToken


def check_login_status():
    print('Checking login status')
    auth_token = request.json['accessToken']
    if auth_token:
        resp = decode_auth_token(auth_token)
        if not isinstance(resp, str):
            if not check_blacklist(auth_token):
                try:
                    responseObject = {
                        'status': 'success',
                        'isUserLoggedIn': True,
                    }
                    resp = make_response(jsonify(responseObject))
                    return resp, 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'isUserLoggedIn': False,
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                try:
                    responseObject = {
                        'status': 'fail',
                        'isUserLoggedIn': False,
                    }
                    resp = make_response(jsonify(responseObject))
                    return resp, 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'isUserLoggedIn': False,
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'isUserLoggedIn': False,
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'isUserLoggedIn': False,
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403


def refresh_access_token(refresh_token, user_agent):
    print(refresh_token)
    print(user_agent)
    if not check_blacklist(refresh_token):
        token = RefreshToken.query.filter_by(refresh_token=refresh_token)
        if token:
            if token.user_agent == user_agent:
                user_id = token.user_id
                auth_token = encode_auth_token(user_id, 60 * 30)  # accessToken
                responseObject = {
                    'status': 'success',
                    'accessToken': auth_token.decode(),
                    'message': 'A new access token was issued.'
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User agent is invalid'
                }
                return make_response(jsonify(responseObject)), 500
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Refresh token is invalid'
            }
            return make_response(jsonify(responseObject)), 500
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Refresh token is in blacklist'
        }
        return make_response(jsonify(responseObject)), 500


def login(email, password):
    print('Logging in')
    try:
        # fetch the user data
        user = User.query.filter_by(
            email=email
        ).first()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            raise Exception('Wrong password')
        auth_token = encode_auth_token(user.id, 60 * 30)  # accessToken
        refresh_token = encode_auth_token(user_id=user.id, expire_at=60 * 60 * 24 * 60)  # refreshToken
        # save refresh token in database
        refresh_token_object = RefreshToken(refresh_token=refresh_token, user_id=user.id,
                                            user_agent=request.user_agent.string,
                                            expires_in=60 * 60 * 24 * 60, ip=request.remote_addr)
        db.session.add(refresh_token_object)
        db.session.commit()
        if auth_token:
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'user_id': user.id,
                'auth_token': auth_token.decode(),
            }
            resp = make_response(jsonify(responseObject))
            # save refresh token in httpOnly cookie available only in auth module
            resp.set_cookie('refreshToken', refresh_token.decode(), httponly=True, path='/api/auth')
            return resp, 200
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500


def register(username, first_name, last_name, email, password, status):
    print('Registering')
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    responseObject = {}
    user = User.query.filter_by(email=email).first()
    if not user:
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=password_hash,
                status=status
            )

            # insert the user
            db.session.add(user)
            db.session.commit()
            # generate the auth token
            auth_token = encode_auth_token(user_id=user.id, expire_at=60 * 30)  # accessToken
            refresh_token = encode_auth_token(user_id=user.id, expire_at=60 * 60 * 24 * 60)  # refreshToken
            # save refresh token in database
            refresh_token_object = RefreshToken(refresh_token=refresh_token, user_id=user.id,
                                                user_agent=request.user_agent.string,
                                                expires_in=60 * 60 * 24 * 60, ip=request.remote_addr)
            db.session.add(refresh_token_object)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'user_id': user.id,
                'auth_token': auth_token.decode(),
                'refresh_token': refresh_token.decode()
            }
            resp = make_response(jsonify(responseObject))
            # save refresh token in httpOnly cookie available only in auth module
            resp.set_cookie('refreshToken', refresh_token.decode(), httponly=True, path='/api/auth')
            return resp, 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202


def logout():
    print('Logging out')
    auth_token = request.json['accessToken']
    refresh_token = request.cookies.get('refreshToken')
    if auth_token:
        resp = decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark both tokens as blacklisted
            blacklist_access_token = BlacklistToken(token=auth_token)
            blacklist_refresh_token = BlacklistToken(token=refresh_token)
            # and remove refresh token from a list of active refresh tokens
            refresh_token_object = RefreshToken.query.filter_by(refresh_token=refresh_token)
            db.session.delete(refresh_token_object)
            db.session.commit()

            try:
                # insert tokens
                db.session.add(blacklist_access_token)
                db.session.add(blacklist_refresh_token)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                resp = make_response(jsonify(responseObject))
                # remove refresh toke from cookies
                resp.set_cookie('refreshToken', '', max_age=0)
                return resp, 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403


def get_current_user_profile():
    print('Getting current user profile')
    auth_token = request.json['accessToken']
    if auth_token:
        resp = decode_auth_token(auth_token)
        print('---')
        print(resp)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'status': user.status,
                    'username': user.username,
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401
