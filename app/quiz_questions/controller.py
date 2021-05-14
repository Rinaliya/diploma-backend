from app import app, db, QuizQuestion
from flask import jsonify, request

from app.auth.authorized_decorator import authorized

PREFIX = '/api/quiz-questions'


@app.route(PREFIX, methods=['GET'])
def get_all_quiz_questions():
    quiz_questions = QuizQuestion.query.all()
    if quiz_questions:
        quiz_questions_list = [quiz_question.to_dict() for quiz_question in quiz_questions]
        return jsonify(quiz_questions_list)
    else:
        return jsonify([])


@app.route(PREFIX + '/<id>', methods=['GET'])
def get_quiz_question_by_id(id):
    quiz_question = QuizQuestion.query.filter(QuizQuestion.id == id).first()
    if quiz_question:
        quiz_question_dict = quiz_question.to_dict()
        return jsonify(quiz_question_dict)
    else:
        return jsonify({})


# @authorized
@app.route(PREFIX, methods=['POST'])
def create_quiz_question():
    data = request.json
    question = data['question']
    answer1 = data['answer1']
    answer2 = data['answer2']
    answer3 = data['answer3']
    answer4 = data['answer4']
    correct_answer = data['correctAnswer']
    locale = data['locale']
    quiz_id = data['quizId']
    quiz_question = QuizQuestion(question=question, answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4,
                                 correct_answer=correct_answer, locale=locale, quiz_id=quiz_id)
    db.session.add(quiz_question)
    db.session.commit()
    return jsonify({'status': 'success'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['PUT'])
def edit_quiz_question_by_id(id):
    data = request.json
    question = data['question']
    answer1 = data['answer1']
    answer2 = data['answer2']
    answer3 = data['answer3']
    answer4 = data['answer4']
    correct_answer = data['correctAnswer']
    locale = data['locale']
    quiz_id = data['quizId']
    quiz_question = QuizQuestion.query.filter(QuizQuestion.id == id).first()
    if quiz_question:
        if question:
            quiz_question.question = question
        if answer1:
            quiz_question.answer1 = answer1
        if answer2:
            quiz_question.answer2 = answer2
        if answer3:
            quiz_question.answer3 = answer3
        if answer4:
            quiz_question.answer4 = answer4
        if correct_answer:
            quiz_question.correct_answer = correct_answer
        if locale:
            quiz_question.locale = locale
        if quiz_id:
            quiz_question.quiz_id = quiz_id
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


# @authorized
@app.route(PREFIX + '/<id>', methods=['DELETE'])
def delete_quiz_question_by_id(id):
    quiz_question = QuizQuestion.query.filter(QuizQuestion.id == id).first()
    if quiz_question:
        db.session.delete(quiz_question)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})
