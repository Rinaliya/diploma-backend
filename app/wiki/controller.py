
from app import app, db, WikiPage
from flask import jsonify, request


@app.route('/api/wiki', methods=['GET'])
def get_all_wiki_pages():
    locale = request.args.get('locale')
    if locale:
        pages = WikiPage.query.filter(WikiPage.locale == locale)
    else:
        pages = WikiPage.query.all()
    if pages:
        pages_list = [page.to_dict() for page in pages]
        print(pages_list)
        return jsonify(pages_list)
    else:
        return jsonify([])


@app.route('/api/wiki/<id>', methods=['GET'])
def get_wiki_page_by_id(id):
    page = WikiPage.query.filter(WikiPage.id == id).first()
    if page:
        page_dict = page.to_dict()
        return jsonify(page_dict)
    else:
        return jsonify({})


@app.route('/api/wiki/slug/<slug>', methods=['GET'])
def get_wiki_page_by_slug(slug):
    page = WikiPage.query.filter(WikiPage.slug == slug).first()
    if page:
        page_dict = page.to_dict()
        return jsonify(page_dict)
    else:
        return jsonify({})


@app.route('/api/wiki', methods=['POST'])
def create_wiki_page():
    data = request.json
    slug = data['slug']
    title = data['title']
    content = data['content']
    locale = data['locale']
    is_visible = data['is_visible']
    page = WikiPage( slug=slug, title=title, content=content, locale=locale, is_visible=is_visible)
    db.session.add(page)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/api/wiki/<id>', methods=['PUT'])
def edit_wiki_page_by_id(id):
    data = request.json
    slug = data['slug']
    title = data['title']
    content = data['content']
    locale = data['locale']
    is_visible = data['is_visible']
    page = WikiPage.query.filter(WikiPage.id == id).first()
    if page:
        if slug:
            page.slug = slug
        if title:
            page.title = title
        if content:
            page.content = content
        if locale:
            page.locale = locale
        page.is_visible = is_visible

        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


@app.route('/api/wiki/<id>', methods=['DELETE'])
def delete_wiki_page_by_id(id):
    page = WikiPage.query.filter(WikiPage.id == id).first()
    if page:
        db.session.delete(page)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})