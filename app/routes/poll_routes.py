from http import HTTPStatus
from http.client import BAD_REQUEST
from flask import Blueprint, request, jsonify
from app.services.poll_service import create_poll, delete_poll, list_all_polls, list_poll_by_id
from database.models import Poll
from database.database import db

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
    
@poll_bp.route("/", methods=['GET'])
def list_polls_route():
    try:
        polls = list_all_polls()
        return jsonify([{
            "id": poll.id,
            "title": poll.title,
            "description": poll.description
        } for poll in polls]), HTTPStatus.OK

    except Exception as e:
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    
@poll_bp.route("/<int:poll_id>", methods=['GET'])
def list_poll_route(poll_id):
    try:
        if poll_id <= 0:
            return error_response("Invalid poll ID", HTTPStatus.BAD_REQUEST)
        
        poll = list_poll_by_id(poll_id)

        if not poll:
            return jsonify({
                "message": f"Poll with ID {poll_id} not found"}), HTTPStatus.NOT_FOUND

        return jsonify({
            "id": poll.id,
            "title": poll.title,
            "description": poll.description
        }), HTTPStatus.OK

    except Exception as e:
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

@poll_bp.route("/<int:poll_id>", methods=["DELETE"])
def delete_poll_route(poll_id):

    try:
        if poll_id <= 0:
            return error_response(f"Invalid poll ID", HTTPStatus.BAD_REQUEST)
    
        poll_deleted = delete_poll(poll_id)

        if not poll_deleted:
            return error_response(f"Poll with ID {poll_id} not found", HTTPStatus.NOT_FOUND)
        
        return jsonify({"message":"Poll deleted with success"}), 200
        
    except Exception as e:
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)