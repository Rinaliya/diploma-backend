from app import app, db, Character
from flask import jsonify, request

from app.auth.authorized_decorator import authorized

PREFIX = '/api/characters'


@app.route(PREFIX, methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    locale = request.args.get('locale')
    if characters:
        characters_list = [character.to_dict() for character in characters]
        if locale:
            characters_list = [c for c in filter(lambda c: c['locale'] == locale, characters_list)]
        return jsonify(characters_list)
    else:
        return jsonify([])


@app.route(PREFIX + '/<id>', methods=['GET'])
def get_character_by_id(id):
    character = Character.query.filter(Character.id == id).first()
    if character:
        character_dict = character.to_dict()
        return jsonify(character_dict)
    else:
        return jsonify({})


# @authorized
@app.route(PREFIX, methods=['POST'])
def create_character():
    data = request.json
    name = data['name']
    description = data['description']
    avatar_image = data['avatar_image']
    full_image = data['full_image']
    locale = data['locale']
    character = Character(name=name, description=description, locale=locale, avatar_image=avatar_image,
                          full_image=full_image)
    db.session.add(character)
    db.session.commit()
    return jsonify({'status': 'success'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['PUT'])
def edit_character_by_id(id):
    data = request.json
    name = data['name']
    description = data['description']
    avatar_image = data['avatar_image']
    full_image = data['full_image']
    locale = data['locale']
    character = Character.query.filter(Character.id == id).first()
    if character:
        if name:
            character.name = name
        if description:
            character.description = description
        if avatar_image:
            character.avatar_image = avatar_image
        if full_image:
            character.full_image = full_image
        if locale:
            character.locale = locale
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['DELETE'])
def delete_character_by_id(id):
    character = Character.query.filter(Character.id == id).first()
    if character:
        db.session.delete(character)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})
