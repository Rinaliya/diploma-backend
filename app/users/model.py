import json

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    first_name = db.Column(db.String(30), index=True)
    last_name = db.Column(db.String(30), index=True)
    email = db.Column(db.String(100), index=True)
    password_hash = db.Column(db.String(10000))
    registered_at = db.Column(db.DateTime)
    can_create_users = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User id: {}, email: {}>'.format(self.id, self.email)

    def to_dict(self):
        user = {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'can_create_users': self.can_create_users,
            'registered_at': self.registered_at,
        }
        return user
