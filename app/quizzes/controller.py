from app import app, db, Quiz, QuizQuestion
from flask import jsonify, request

from app.auth.authorized_decorator import authorized

PREFIX = '/api/quizzes'


@app.route(PREFIX, methods=['GET'])
def get_all_quizzes():
    quizzes = Quiz.query.all()
    if quizzes:
        quizzes_list = [quiz.to_dict() for quiz in quizzes]
        return jsonify(quizzes_list)
    else:
        return jsonify([])


@app.route(PREFIX + '/<id>', methods=['GET'])
def get_quizzes_by_id(id):
    quiz = Quiz.query.filter(Quiz.id == id).first()
    if quiz:
        quiz_dict = quiz.to_dict()
        return jsonify(quiz_dict)
    else:
        return jsonify({})


@app.route(PREFIX + '/slug/<slug>', methods=['GET'])
def get_quizzes_by_slug(slug):
    quiz = Quiz.query.filter(Quiz.slug == slug).first()
    if quiz:
        quiz_dict = quiz.to_dict()
        return jsonify(quiz_dict)
    else:
        return jsonify({})


@app.route(PREFIX + '/questions/<id>', methods=['GET'])
def get_quiz_question_by_quiz_id(id):
    quiz = Quiz.query.filter(Quiz.id == id).first()
    if quiz:
        quiz_dict = quiz.to_dict()
        return jsonify(quiz_dict['questions'])
    else:
        return jsonify([])


# @authorized
@app.route(PREFIX, methods=['POST'])
def create_quiz():
    data = request.json
    title = data['title']
    slug = data['slug']
    cover = data['cover']
    is_visible = data['is_visible']
    locale = data['locale']
    questions = data['questions']
    quiz = Quiz(title=title, slug=slug, cover=cover, locale=locale, is_visible=is_visible)
    db.session.add(quiz)
    db.session.commit()
    for q in questions:
        print(questions)
        question_object = QuizQuestion(question=q['question'], answer1=q['answer1'], answer2=q['answer2'],
                                       answer3=q['answer3'], answer4=q['answer4'], correct_answer=q['correctAnswer'],
                                       quiz_id=quiz.id, locale=quiz.locale)
        db.session.add(question_object)
    db.session.commit()
    return jsonify({'status': 'success'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['PUT'])
def edit_quiz_by_id(id):
    data = request.json
    title = data['title']
    slug = data['slug']
    cover = data['cover']
    is_visible = data['is_visible']
    locale = data['locale']
    questions = data['questions']
    quiz = Quiz.query.filter(Quiz.id == id).first()
    old_questions = quiz.questions
    for question in old_questions:
        db.session.delete(question)
    if quiz:
        if title:
            quiz.title = title
        if slug:
            quiz.slug = slug
        if cover:
            quiz.cover = cover
        if locale:
            quiz.locale = locale
        if is_visible is not None:
            quiz.is_visible = is_visible
        for q in questions:
            print(q)
            print(quiz.id)
            question_object = QuizQuestion(question=q['question'], answer1=q['answer1'], answer2=q['answer2'],
                                           answer3=q['answer3'], answer4=q['answer4'],
                                           correct_answer=q['correctAnswer'], quiz_id=id,
                                           locale=quiz.locale)
            db.session.add(question_object)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['DELETE'])
def delete_quiz_by_id(id):
    quiz = Quiz.query.filter(Quiz.id == id).first()
    if quiz:
        quiz_questions = quiz.questions
        for question in quiz_questions:
            db.session.delete(question)
        db.session.delete(quiz)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})
