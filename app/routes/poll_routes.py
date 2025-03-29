from http import HTTPStatus
from flask import Blueprint, request, jsonify
from app.services.poll_service import create_poll
from database.models import Poll

poll_bp = Blueprint('polls', __name__)

@poll_bp.route("/", methods=['POST'])
def create_poll_route():
    try:
        data = request.get_json()
        poll = create_poll(data['title'], data['description'])
        
        return jsonify({"message": "Poll created",
                        "data": {
                            "id": poll.id,
                            "title": poll.title,
                            "description": poll.description                
                        }}), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR