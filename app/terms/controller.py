from app import app, db, Term
from flask import jsonify, request

@app.route('/api/terms', methods=['GET'])
def get_all_terms():
    terms = Term.query.all()
    if terms:
        term_list = [terms.to_dict() for terms in terms]
        print(term_list)
        return jsonify(term_list)
    else:
        return jsonify([])


@app.route('/api/terms/<id>', methods=['GET'])
def get_terms_by_id(id):
    term = Term.query.filter(Term.id == id).first()
    if term:
        term_dict = term.to_dict()
        return jsonify(term_dict)
    else:
        return jsonify({})


@app.route('/api/terms', methods=['POST'])
def create_terms():
    data = request.json
    term = data['term']
    definition = data['definition']
    locale = data['locale']
    terms = Term( term=term, definition=definition, locale=locale)
    db.session.add(terms)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/api/terms/<id>', methods=['PUT'])
def edit_terms_by_id(id):
    data = request.json
    term = data['term']
    definition = data['definition']
    locale = data['locale']
    terms = Term.query.filter(Term.id == id).first()
    if terms:
        if term:
            terms.term = term
        if definition:
            terms.definition = definition
        if locale:
            terms.locale = locale

        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})

@app.route('/api/terms/<id>', methods=['DELETE'])
def delete_terms_by_id(id):
    term = Term.query.filter(Term.id == id).first()
    if term:
        db.session.delete(term)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})