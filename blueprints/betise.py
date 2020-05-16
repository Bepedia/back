from flask import Blueprint, jsonify, request
from controllers import FirestoreIO, StorageIO

collection = 'betise'

betise_bp = Blueprint(collection, __name__)


@betise_bp.route('')
def get_recettes():
    firestore_io = FirestoreIO()
    return jsonify(firestore_io.list(collection))


@betise_bp.route('/<doc_id>')
def get(doc_id):
    firestore_io = FirestoreIO()
    return jsonify(firestore_io.get(collection, doc_id))


@betise_bp.route('', methods=['POST'])
def create():
    firestore_io = FirestoreIO()
    return jsonify(firestore_io.insert(collection, request.get_json()))


@betise_bp.route('/<doc_id>', methods=['PATCH'])
def update(doc_id):
    firestore_io = FirestoreIO()
    return jsonify(firestore_io.update(collection, doc_id, request.get_json()))


@betise_bp.route('/<doc_id>/image', methods=['POST'])
def upload_image(doc_id):
    storage_io = StorageIO()
    firestore_io = FirestoreIO()
    file = request.files['file']
    url = storage_io.post_img(file, collection + '/' + doc_id + '.' + file.content_type.replace('image/', ''))
    doc = firestore_io.get(collection, doc_id)
    doc.update({'img_url': url})
    return jsonify(firestore_io.update(collection, doc_id, doc))
