from app import db


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), index=True)
    description = db.Column(db.String(10000), index=True)
    cover = db.Column(db.String(10000), index=True)
    slug = db.Column(db.String(10000), index=True)
    locale = db.Column(db.String(10), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('game_categories.id'))

    def __repr__(self):
        return '<Game id: {}, title: {}>'.format(self.id, self.title)

    def to_dict(self):
        game = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'cover': self.cover,
            'locale': self.locale,
            'slug': self.slug,
            'category': self.category.to_dict(),
            'category_id': self.category_id
        }
        return game


