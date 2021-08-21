from flask import Blueprint, jsonify, request
from controllers import FirestoreIO, StorageIO
from datetime import datetime
import uuid

from controllers.user_io import get_user

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
    document = request.get_json()
    document["creation_date"] = datetime.now().isoformat()
    document["author"] = get_user(request.headers)
    document["comments"] = []
    return jsonify(firestore_io.insert(collection, document))


@betise_bp.route('/<doc_id>', methods=['PATCH'])
def update(doc_id):
    firestore_io = FirestoreIO()
    return jsonify(firestore_io.update(collection, doc_id, request.get_json()))


@betise_bp.route('/<doc_id>/comment', methods=['POST'])
def comment(doc_id):
    comment = request.get_json()
    comment["creation_date"] = datetime.now().isoformat()
    comment["author"] = get_user(request.headers)
    comment["id"] = str(uuid.uuid4())
    firestore_io = FirestoreIO()
    item = firestore_io.get(collection, doc_id)

    if "comments" not in item:
        item["comments"] = []

    item["comments"].append(comment)
    return jsonify(firestore_io.update(collection, doc_id, item))


@betise_bp.route('/<doc_id>/comment/<comment_id>', methods=['DELETE'])
def delete_comment(doc_id, comment_id):
    firestore_io = FirestoreIO()
    item = firestore_io.get(collection, doc_id)
    for c in item.get("comments", []):
        if c.get("id") == comment_id:
            item["comments"].remove(c)
    return jsonify(firestore_io.update(collection, doc_id, item))


@betise_bp.route('/<doc_id>', methods=['DELETE'])
def delete(doc_id):
    firestore_io = FirestoreIO()
    return jsonify(firestore_io.delete(collection, doc_id))


@betise_bp.route('/<doc_id>/image', methods=['POST'])
def upload_image(doc_id):
    storage_io = StorageIO()
    firestore_io = FirestoreIO()
    file = request.files['file']
    url = storage_io.post_img(file, file.content_type.replace('image/', ''), collection)
    doc = firestore_io.get(collection, doc_id)
    doc.update({'img_url': url})
    return jsonify(firestore_io.update(collection, doc_id, doc))
