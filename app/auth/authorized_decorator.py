def authorized(func):
    # from flask import flask, request
    import flask
    from app.auth.tokens_utils import decode_auth_token
    def wrapper(*args, **kwargs):
        # get user info
        auth_token = flask.request.get_json()['accessToken'] if flask.request.get_json() else None
        author_id = None
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                author_id = resp
            else:
                # if unauthorized - return error 403
                # raise Exception('Unauthorized user')
                return 'Unauthorized access is restricted', 403
            # else run passed function
            return func(*args, **kwargs)
        else:
            # if unauthorized - return error 403
            return 'Unauthorized access is restricted', 403
    return wrapper
