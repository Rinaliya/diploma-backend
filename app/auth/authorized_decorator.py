def authorized(func):
    # from flask import flask, request
    import flask
    from app.auth.tokens_utils import decode_auth_token
    def wrapper(*args, **kwargs):
        print('wrapper function')
        # get user info
        print(flask.request.get_json())
        auth_token = flask.request.get_json()['accessToken'] if flask.request.get_json() else None
        # auth_token = request.json['accessToken']
        print('auth token = ', auth_token)
        author_id = None
        if auth_token:
            print('auth token found')
            resp = decode_auth_token(auth_token)
            print('resp = ', resp)
            if not isinstance(resp, str):
                author_id = resp
                print('author_id = ', author_id)
            else:
                # if unauthorized - return error 403
                # raise Exception('Unauthorized user')
                print('problem with resp, return 403 unauthorized, resp = ', resp)
                return 'Unauthorized access is restricted', 403
            # else run passed function
            print('authorized, running passed function')
            return func(*args, **kwargs)
        else:
            # if unauthorized - return error 403
            print('no token found, return 403 unauthorized')
            return 'Unauthorized access is restricted', 403
    return wrapper
