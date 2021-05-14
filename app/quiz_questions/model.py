from app import db


class QuizQuestion(db.Model):
    __tablename__ = 'quizquestions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(10000), index=True)
    answer1 = db.Column(db.String(10000), index=True)
    answer2 = db.Column(db.String(10000), index=True)
    answer3 = db.Column(db.String(10000), index=True)
    answer4 = db.Column(db.String(10000), index=True)
    correct_answer = db.Column(db.Integer, index=True)
    locale = db.Column(db.String(10), index=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))

    def __repr__(self):
        return '<Quiz id: {}, title: {}>'.format(self.id, self.question)

    def to_dict(self):
        quiz = {
            'id': self.id,
            'question': self.question,
            'answer1': self.answer1,
            'answer2': self.answer2,
            'answer3': self.answer3,
            'answer4': self.answer4,
            'correct_answer': self.correct_answer,
            'locale': self.locale,
            'quiz_id': self.quiz_id,
            # 'lecture': self.lecture.to_dict()
        }
        return quiz


