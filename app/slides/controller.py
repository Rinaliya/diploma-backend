from app import app, db, Slide
from flask import jsonify, request

from app.auth.authorized_decorator import authorized

PREFIX = '/api/slide-types'


@app.route(PREFIX, methods=['GET'])
def get_all_slides():
    slides = Slide.query.all()
    if slides:
        categories_list = [slide.to_dict() for slide in slides]
        return jsonify(categories_list)
    else:
        return jsonify([])


@app.route(PREFIX + '/<id>', methods=['GET'])
def get_slide_by_id(id):
    slide = Slide.query.filter(Slide.id == id).first()
    if slide:
        slide_dict = slide.to_dict()
        return jsonify(slide_dict)
    else:
        return jsonify({})


# @authorized
@app.route(PREFIX, methods=['POST'])
def create_slide():
    data = request.json
    order = data['order']
    background = data['background']
    content = data['content']
    payload = data['payload']
    locale = data['locale']
    is_visible = data['is_visible']
    lecture_id = data['lecture_id']
    slide_type_id = data['slide_type_id']
    character_id = data['character_id']
    slide = Slide(order=order, background=background, content=content, payload=payload, locale=locale,
                  is_visible=is_visible, lecture_id=lecture_id, slide_type_id=slide_type_id, character_id=character_id)
    db.session.add(slide)
    db.session.commit()
    return jsonify({'status': 'success'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['PUT'])
def edit_slide_by_id(id):
    data = request.json
    order = data['order']
    background = data['background']
    content = data['content']
    payload = data['payload']
    locale = data['locale']
    is_visible = data['is_visible']
    lecture_id = data['lecture_id']
    slide_type_id = data['slide_type_id']
    character_id = data['character_id']
    slide = Slide.query.filter(Slide.id == id).first()
    if slide:
        if order:
            slide.order = order
        if background:
            slide.background = background
        if content:
            slide.content = content
        if payload:
            slide.payload = payload
        if locale:
            slide.locale = locale
        if is_visible is not None:
            slide.is_visible = is_visible
        if lecture_id:
            slide.lecture_id = lecture_id
        if slide_type_id:
            slide.slide_type_id = slide_type_id
        if character_id:
            slide.character_id = character_id
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['DELETE'])
def delete_slide_by_id(id):
    slide = Slide.query.filter(Slide.id == id).first()
    if slide:
        db.session.delete(slide)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})
