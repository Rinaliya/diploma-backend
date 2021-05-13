from app import app, db, SlideType
from flask import jsonify, request

from app.auth.authorized_decorator import authorized

PREFIX = '/api/slide-types'


@app.route(PREFIX, methods=['GET'])
def get_all_slide_types():
    slide_types = SlideType.query.all()
    if slide_types:
        categories_list = [slide_type.to_dict() for slide_type in slide_types]
        return jsonify(categories_list)
    else:
        return jsonify([])


@app.route(PREFIX + '/<id>', methods=['GET'])
def get_slide_type_by_id(id):
    slide_type = SlideType.query.filter(SlideType.id == id).first()
    if slide_type:
        slide_type_dict = slide_type.to_dict()
        return jsonify(slide_type_dict)
    else:
        return jsonify({})


# @authorized
@app.route(PREFIX, methods=['POST'])
def create_slide_type():
    data = request.json
    title = data['title']
    description = data['description']
    slide_type = SlideType(title=title, description=description)
    db.session.add(slide_type)
    db.session.commit()
    return jsonify({'status': 'success'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['PUT'])
def edit_slide_type_by_id(id):
    data = request.json
    title = data['title']
    description = data['description']
    slide_type = SlideType.query.filter(SlideType.id == id).first()
    if slide_type:
        if title:
            slide_type.title = title
        if description:
            slide_type.description = description
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['DELETE'])
def delete_slide_type_by_id(id):
    slide_type = SlideType.query.filter(SlideType.id == id).first()
    if slide_type:
        db.session.delete(slide_type)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})
