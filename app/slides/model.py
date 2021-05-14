from app import db


class Slide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, index=True)
    background = db.Column(db.String(1000), index=True)
    content = db.Column(db.String(10000), index=True)
    payload = db.Column(db.String(10000), index=True)
    locale = db.Column(db.String(10), index=True)
    is_visible = db.Column(db.Boolean, index=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    slide_type_id = db.Column(db.Integer, db.ForeignKey('slidetype.id'))

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
            'lecture_id': self.lecture_id,
            'character_id': self.character_id,
            'character': self.character,
            'slide_type_id': self.slide_type_id
        }
        return slide

