from app import db


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(1000), index=True)
    title = db.Column(db.String(1000), index=True)
    cover = db.Column(db.String(10000), index=True)
    locale = db.Column(db.String(10), index=True)
    is_visible = db.Column(db.Boolean, index=True)
    questions = db.relationship('QuizQuestion', backref='quiz', lazy='dynamic')
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))

    def __repr__(self):
        return '<Quiz id: {}, title: {}>'.format(self.id, self.title)

    def to_dict(self):
        quiz = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'cover': self.cover,
            'locale': self.locale,
            'is_visible': self.is_visible,
            'lecture_id': self.lecture_id,
            'questions': self.questions
        }
        return quiz


