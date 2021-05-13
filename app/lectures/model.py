from app import db


class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(1000), index=True)
    title = db.Column(db.String(1000), index=True)
    locale = db.Column(db.String(10), index=True)
    is_visible = db.Column(db.Boolean, index=True)
    order = db.Column(db.Integer, index=True)
    slides = db.relationship('Slide', backref='lecture', lazy='dynamic')

    def __repr__(self):
        return '<Lecture id: {}, title: {}>, order: {}'.format(self.id, self.title, self.order)

    def to_dict(self):
        lecture = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'locale': self.locale,
            'is_visible': self.is_visible,
            'order': self.order
        }
        return lecture


