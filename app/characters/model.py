from app import db


class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), index=True)
    description = db.Column(db.String(10000), index=True)
    avatar_image = db.Column(db.String(10000), index=True)
    full_image = db.Column(db.String(10000), index=True)
    locale = db.Column(db.String(10), index=True)
    slides = db.relationship('Slide', backref='character', lazy='dynamic')

    def __repr__(self):
        return '<Character id: {}, name: {}>, description: {}'.format(self.id, self.name, self.description)

    def to_dict(self):
        character = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'locale': self.locale,
            'avatar_image': self.avatar_image,
            'full_image': self.full_image
        }
        return character


