from flask import Blueprint, jsonify, request
from controllers import FirestoreIO, StorageIO

collection = 'galerie'

galerie_bp = Blueprint(collection, __name__)


@galerie_bp.route('')
def list():
    firestore_io = FirestoreIO()
    return jsonify(firestore_io.list(collection))


@galerie_bp.route('/<doc_id>', methods=['DELETE'])
def delete(doc_id):
    firestore_io = FirestoreIO()
    return jsonify(firestore_io.delete(collection, doc_id))


@galerie_bp.route('/image', methods=['POST'])
def upload_image():
    storage_io = StorageIO()
    firestore_io = FirestoreIO()
    file = request.files['file']
    url = storage_io.post_img(file, file.content_type.replace('image/', ''), collection)
    return firestore_io.insert(collection, {'url': url})

