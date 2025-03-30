from http import HTTPStatus
from http.client import BAD_REQUEST
from flask import Blueprint, request, jsonify
from app.services.poll_service import create_poll, create_poll_option, delete_poll, delete_poll_option, list_all_polls, list_poll_by_id, list_poll_options, vote_on_poll
from database.models import Poll, PollOption
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

        options = []
        for option in poll.options:
            options.append({
                "id": option.option_id,
                "description": option.description
            })

        return jsonify({
            "id": poll.id,
            "title": poll.title,
            "description": poll.description,
            "options": options
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
    
@poll_bp.route("/<int:poll_id>/opcoes", methods=["POST"])
def add_option_route(poll_id):
    try:
        if poll_id <= 0:
            return error_response("Invalid poll ID", HTTPStatus.BAD_REQUEST)

        data = request.get_json()

        if not data:
            return error_response(str("error"), HTTPStatus.BAD_REQUEST)

        new_option = create_poll_option(poll_id=poll_id, description=data["description"])

        return jsonify({"message": "Poll option added with success",
                        "data": {
                            "id": new_option.option_id,
                            "poll_id": new_option.poll_id,
                            "description": new_option.description
                        }}), 201

    except Exception as e:
        return error_response(f"An unexpected error ocurred. {e}", HTTPStatus.INTERNAL_SERVER_ERROR)

@poll_bp.route("/<int:poll_id>/opcoes", methods=["GET"])
def list_poll_options_route(poll_id):
    try:
        if poll_id <= 0:
            return error_response("Invalid poll ID", HTTPStatus.BAD_REQUEST)

        options = list_poll_options(poll_id)

        options_list = [{
            "id": option.option_id,
            "description": option.description
        } for option in options]

        return jsonify({
            "poll_id": poll_id,
            "options": options_list
        }), HTTPStatus.OK
    
    except Exception as e:
        return error_response(f"An unexpected error ocurred. {e}", HTTPStatus.INTERNAL_SERVER_ERROR)

@poll_bp.route("/<int:poll_id>/opcoes/<int:option_id>", methods=["DELETE"])
def delete_poll_option_route(poll_id: int, option_id: int):
    try:
        if poll_id <= 0 or option_id <= 0:
            return error_response("Invalid poll or option ID", HTTPStatus.BAD_REQUEST)

        option_deleted = delete_poll_option(poll_id, option_id)

        if not option_deleted:
            return error_response(
                f"Option with ID {option_id} not found in poll {poll_id}", 
                HTTPStatus.NOT_FOUND
            )

        return jsonify({
            "message": "Poll option deleted successfully",
            "data": {
                "poll_id": poll_id,
                "option_id": option_id
            }
        }), HTTPStatus.OK

    except Exception as e:
        return error_response(f"An unexpected error ocurred. {e}", HTTPStatus.INTERNAL_SERVER_ERROR)

@poll_bp.route("/<int:poll_id>/votar", methods=["POST"])
def vote_on_poll_route(poll_id: int):
    try:
        if poll_id <= 0:
            return error_response("Invalid poll ID", HTTPStatus.BAD_REQUEST)
  
        data = request.get_json()
        if not data:
            return error_response("No input data provided", HTTPStatus.BAD_REQUEST)

        vote = vote_on_poll(
            user_id=data['user_id'],
            poll_id=poll_id,
            option_id=data['option_id']
        )

        return jsonify({
            "message": "Vote registered successfully",
            "data": {
                "vote_id": vote.vote_id,
                "user_id": vote.user_id,
                "poll_id": poll_id,
                "option_id": vote.poll_option_id,
                "voted_at": vote.vote_at.isoformat()
            }
        }), HTTPStatus.CREATED

    except Exception as e:
        return error_response(f"An unexpected error ocurred. {e}", HTTPStatus.INTERNAL_SERVER_ERROR)