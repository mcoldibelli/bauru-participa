from http import HTTPStatus
from http.client import BAD_REQUEST
from flask import Blueprint, request, jsonify
from app.services.poll_service import create_poll
from database.models import Poll

poll_bp = Blueprint('polls', __name__)

def error_response(message: str, status_code: int):
    return jsonify({"error": str(message)}), status_code

@poll_bp.route("/", methods=['POST'])
def create_poll_route():
    try:
        data = request.get_json()

        if not data:
            return error_response(str(e), HTTPStatus.BAD_REQUEST)

        poll = create_poll(data['title'], data['description'])

        return jsonify({"message": "Poll created",
                        "data": {
                            "id": poll.id,
                            "title": poll.title,
                            "description": poll.description                
                        }}), HTTPStatus.CREATED
    
    except Exception as e:
         return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)