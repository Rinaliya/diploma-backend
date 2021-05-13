from app import db


class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(10000), index=True)
    answer1 = db.Column(db.String(10000), index=True)
    answer2 = db.Column(db.String(10000), index=True)
    answer3 = db.Column(db.String(10000), index=True)
    answer4 = db.Column(db.String(10000), index=True)
    correct_answer = db.Column(db.String(10000), index=True)
    locale = db.Column(db.String(10), index=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

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
            # 'lecture': self.lecture.to_dict()
        }
        return quiz


