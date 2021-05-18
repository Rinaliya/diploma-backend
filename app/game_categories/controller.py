from app import app, db, Game, GameCategory
from flask import jsonify, request

from app.auth.authorized_decorator import authorized

PREFIX = '/api/game-categories'


@app.route(PREFIX, methods=['GET'])
def get_all_game_categories():
    game_categories = GameCategory.query.all()
    locale = request.args.get('locale')
    if game_categories:
        categories_list = [category.to_dict() for category in game_categories]
        if locale:
            categories_list = [c for c in filter(lambda c: c['locale'] == locale, categories_list)]
        return jsonify(categories_list)
    else:
        return jsonify([])


@app.route(PREFIX + '/<id>', methods=['GET'])
def get_game_category_by_id(id):
    category = GameCategory.query.filter(GameCategory.id == id).first()
    if category:
        category_dict = category.to_dict()
        return jsonify(category_dict)
    else:
        return jsonify({})


@authorized
@app.route(PREFIX, methods=['POST'])
def create_game_category():
    data = request.json
    title = data['title']
    description = data['description']
    locale = data['locale']
    category = GameCategory(title=title, description=description, locale=locale)
    db.session.add(category)
    db.session.commit()
    return jsonify({'status': 'success'})


@authorized
@app.route(PREFIX + '/<id>', methods=['PUT'])
def edit_game_category_by_id(id):
    data = request.json
    title = data['title']
    description = data['description']
    locale = data['locale']
    category = GameCategory.query.filter(GameCategory.id == id).first()
    if category:
        if title:
            category.title = title
        if description:
            category.description = description
        if locale:
            category.locale = locale
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


@authorized
@app.route(PREFIX + '/<id>', methods=['DELETE'])
def delete_game_category_by_id(id):
    category = GameCategory.query.filter(GameCategory.id == id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})