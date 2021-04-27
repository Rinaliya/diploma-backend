from app import db


class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(1000), index=True)
    definition = db.Column(db.String(1000), index=True)
    locale = db.Column(db.String(1000), index=True)

    def __repr__(self):
        return '<Term id: {}, term: {}>'.format(self.id, self.term)

    def to_dict(self):
        term = {
            'id': self.id,
            'term': self.term,
            'definition': self.definition,
            'locale': self.locale,
        }
        return term


