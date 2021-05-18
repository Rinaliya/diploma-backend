from app import app, db, Game, GameCategory
from flask import jsonify, request

from app.auth.authorized_decorator import authorized

PREFIX = '/api/games'


@app.route(PREFIX, methods=['GET'])
def get_all_games():
    games = Game.query.all()
    if games:
        games_list = [game.to_dict() for game in games]
        return jsonify(games_list)
    else:
        return jsonify([])


@app.route(PREFIX + '/<id>', methods=['GET'])
def get_games_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    if game:
        game_dict = game.to_dict()
        return jsonify(game_dict)
    else:
        return jsonify({})


@app.route(PREFIX + '/slug/<slug>', methods=['GET'])
def get_games_by_slug(slug):
    game = Game.query.filter(Game.slug == slug).first()
    if game:
        game_dict = game.to_dict()
        return jsonify(game_dict)
    else:
        return jsonify({})


@authorized
@app.route(PREFIX, methods=['POST'])
def create_game():
    data = request.json
    title = data['title']
    description = data['description']
    cover = data['cover']
    slug = data['slug']
    category_id = data['category_id']
    locale = data['locale']
    # category = GameCategory.query.filter(GameCategory.id == category_id).first()
    game = Game(title=title, description=description, cover=cover, slug=slug, locale=locale, category_id=category_id)
    db.session.add(game)
    db.session.commit()
    return jsonify({'status': 'success'})


@authorized
@app.route(PREFIX + '/<id>', methods=['PUT'])
def edit_game_by_id(id):
    data = request.json
    title = data['title']
    description = data['description']
    cover = data['cover']
    slug = data['slug']
    category_id = data['category_id']
    locale = data['locale']
    game = Game.query.filter(Game.id == id).first()
    if game:
        if title:
            game.title = title
        if description:
            game.description = description
        if cover:
            game.cover = cover
        if slug:
            game.slug = slug
        if locale:
            game.locale = locale
        if category_id:
            # category = GameCategory.query.filter(GameCategory.id == category_id).first()
            # game.category = category
            game.category_id = category_id
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


@authorized
@app.route(PREFIX + '/<id>', methods=['DELETE'])
def delete_game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    if game:
        db.session.delete(game)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})