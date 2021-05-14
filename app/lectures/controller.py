from app import app, db, Lecture, Slide
from flask import jsonify, request

from app.auth.authorized_decorator import authorized

PREFIX = '/api/lectures'


@app.route(PREFIX, methods=['GET'])
def get_all_lectures():
    lectures = Lecture.query.all()
    if lectures:
        lectures_list = [lecture.to_dict() for lecture in lectures]
        return jsonify(lectures_list)
    else:
        return jsonify([])


@app.route(PREFIX + '/<id>', methods=['GET'])
def get_lectures_by_id(id):
    lecture = Lecture.query.filter(Lecture.id == id).first()
    if lecture:
        lecture_dict = lecture.to_dict()
        return jsonify(lecture_dict)
    else:
        return jsonify({})


# @authorized
@app.route(PREFIX, methods=['POST'])
def create_lecture():
    data = request.json
    title = data['title']
    slug = data['slug']
    is_visible = data['is_visible']
    locale = data['locale']
    order = data['order']
    slides = data['slides']
    lecture = Lecture(title=title, slug=slug, order=order, locale=locale, is_visible=is_visible)
    db.session.add(lecture)
    for s in slides:
        slide_object = Slide(order=s['order'], lecture_id=lecture.id, locale=lecture.locale,
                             slide_type_id=s['slide_type_id'], background=s['background'], content=s['content'],
                             payload=s['payload'], character_id=s['character_id'], is_visible=s['is_visible'])
        db.session.add(slide_object)
    db.session.commit()
    return jsonify({'status': 'success'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['PUT'])
def edit_lecture_by_id(id):
    data = request.json
    title = data['title']
    slug = data['slug']
    is_visible = data['is_visible']
    locale = data['locale']
    order = data['order']
    slides = data['slides']
    lecture = Lecture.query.filter(Lecture.id == id).first()
    old_slides = lecture.slides
    for slide in old_slides:
        db.session.delete(slide)
    if lecture:
        if title:
            lecture.title = title
        if slug:
            lecture.slug = slug
        if order:
            lecture.cover = order
        if locale:
            lecture.locale = locale
        if is_visible is not None:
            lecture.is_visible = is_visible
        for s in slides:
            slide_object = Slide(order=s['order'], lecture_id=lecture.id, locale=lecture.locale,
                                 slide_type_id=s['slide_type_id'], background=s['background'], content=s['content'],
                                 payload=s['payload'], character_id=s['character_id'], is_visible=s['is_visible'])
            db.session.add(slide_object)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['DELETE'])
def delete_lecture_by_id(id):
    lecture = Lecture.query.filter(Lecture.id == id).first()
    if lecture:
        db.session.delete(lecture)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})
