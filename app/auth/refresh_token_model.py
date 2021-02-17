import datetime

from app import db


class RefreshToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'refresh_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    refresh_token = db.Column(db.String(500), unique=True, nullable=False)
    user_id = db.Column(db.Integer)
    user_agent = db.Column(db.String(1000))
    ip = db.Column(db.String(20))
    expires_in = db.Column(db.BIGINT)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, refresh_token, user_id, user_agent, expires_in, ip):
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.user_agent = user_agent
        self.expires_in = expires_in
        self.ip = ip
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}>'.format(self.refresh_token)

    def to_dict(self):
        token = {
            'id': self.id,
            'refresh_token': self.refresh_token,
            'user_id': self.user_id,
            'user_agent': self.user_agent,
            'ip': self.ip,
            'expires_in': self.expires_in,
            'created_at': self.created_at
        }
        return token
