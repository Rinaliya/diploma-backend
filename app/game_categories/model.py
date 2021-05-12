from app import db


class GameCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), index=True)
    description = db.Column(db.String(10000), index=True)
    locale = db.Column(db.String(10), index=True)
    games = db.relationship('Game', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<GameCategory id: {}, title: {}>'.format(self.id, self.title)

    def to_dict(self):
        game_category = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'locale': self.locale
        }
        return game_category


