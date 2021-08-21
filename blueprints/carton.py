import os
from flask import Blueprint, jsonify, request
from controllers import FirestoreIO
from controllers.mail_io import send_carton_mail
from controllers.qr_io import generate_qr

carton_bp = Blueprint('carton', __name__)


@carton_bp.route('/<doc_id>/qr', methods=['POST'])
def send_qr(doc_id):
    firestore_io = FirestoreIO()
    carton = firestore_io.get('carton', doc_id)
    to = request.get_json().get("to")
    url = f"{os.environ.get('FRONT_URL')}/cartons/{doc_id}"
    file_name = generate_qr(url)
    send_carton_mail(carton, file_name, to)
    os.remove(file_name)
    return jsonify({})


