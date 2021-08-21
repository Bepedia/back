from flask import Blueprint, jsonify, request

from controllers.user_io import get_user

user_bp = Blueprint('user', __name__)


@user_bp.route('/me')
def get_me():
    return jsonify({
        "email": get_user(request.headers)
    })
