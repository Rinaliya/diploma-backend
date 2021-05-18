from app import db


class Slide(db.Model):
    __tablename__ = 'slides'
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, index=True)
    background = db.Column(db.String(1000), index=True)
    content = db.Column(db.String(10000), index=True)
    payload = db.Column(db.String(10000), index=True)
    locale = db.Column(db.String(10), index=True)
    is_visible = db.Column(db.Boolean, index=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    slide_type_id = db.Column(db.Integer, db.ForeignKey('slidetypes.id'))

    def __repr__(self):
        return '<Slide id: {}, content: {}>, order: {}'.format(self.id, self.content, self.order)

    def to_dict(self):
        slide = {
            'id': self.id,
            'order': self.order,
            'background': self.background,
            'locale': self.locale,
            'is_visible': self.is_visible,
            'content': self.content,
            'payload': self.payload,
            'lecture_id': self.lecture.id,
            'character_id': self.character.id,
            'character': self.character.to_dict(),
            'slide_type_id': self.slide_type.id,
            'slide_type': self.slide_type.to_dict()
        }
        return slide


