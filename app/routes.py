import os
from os import listdir
from os.path import isfile, isdir, join

from app import app


@app.route('/')
@app.route('/index')
def serve():
    return 'Hello from backend'


@app.route('/upload', methods=['POST'])
def upload_image():
    category = request.form.get('category')
    print(category)
    uploads_dir = os.path.join(app.static_folder, 'images', category)
    os.makedirs(uploads_dir, exist_ok=True)
    image = request.files.get('image')
    print(image.filename)
    print(os.path.join(uploads_dir, image.filename))
    image.save(os.path.join(uploads_dir, image.filename))
    return 'ok', 200


@app.route('/get-images', methods=['GET'])
def get_all_uploaded_images():
    images_folder = os.path.join(app.static_folder, 'images')
    categories = [f for f in listdir(images_folder) if isdir(join(images_folder, f))]
    images = {}
    for c in categories:
        images[c] = [f for f in listdir(join(images_folder, c)) if isfile(join(images_folder, c, f))]
    return jsonify(images)


@app.route('/get-images/<category>', methods=['GET'])
def get_images_by_category(category):
    category_folder = os.path.join(app.static_folder, 'images', category)
    if isdir(category_folder):
        images = [f for f in listdir(category_folder) if isfile(join(category_folder, f))]
        return jsonify(images)
    else:
        return 'No such category: ' + category, 404


from app.auth.controller import *
from app.users.controller import *
from app.wiki.controller import *
from app.terms.controller import *
