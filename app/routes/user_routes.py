from http import HTTPStatus
from flask import Blueprint, jsonify, request
from app.services.user_service import UserService

user_bp = Blueprint('users', __name__)

def error_response(message: str, status_code: int):
    return jsonify({"error": str(message)}), status_code

@user_bp.route("/", methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return error_response("Not input data provided", HTTPStatus.BADREQUEST)
    
        user = UserService.create_user(data['name'])

        return jsonify({
            "message": "Poll created with success",
            "data": {
                "id": user.id,
                "name": user.name
            }
        }), HTTPStatus.CREATED

    except Exception as e:
        return error_response("An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR)