from app import db


class SlideType(db.Model):
    __tablename__ = 'slidetypes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), index=True)
    description = db.Column(db.String(10000), index=True)

    def __repr__(self):
        return '<SlideType id: {}, title: {}>, description: {}'.format(self.id, self.title, self.description)

    def to_dict(self):
        slide_type = {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }
        return slide_type


