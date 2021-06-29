from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

#added Bluerprint and one to many relationships between models

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


@boards_bp.route("", methods=["GET"])
def list_all_boards():
    boards_response = [board.as_dict() for board in Board.query.all()]
    return jsonify(boards_response)


@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    if invalid_board_post_request_body(request_body):
        return make_response({"details": "Missing required data"}, 400)

    board = Board(title=request_body["title"], owner=request_body["owner"])

    db.session.add(board)
    db.session.commit()

    return make_response({"id": board.board_id}, 201)


def invalid_board_post_request_body(request_body):
    if ("title" not in request_body or "owner" not in request_body):
        return True
    return False


@boards_bp.route("/<int:board_id>", methods=["GET"])
def get_board_by_id(board_id):
    board = Board.query.get_or_404(board_id)
    return jsonify(board.as_dict_with_cards())


@boards_bp.route("/<int:board_id>", methods=["PUT"])
def update_board(board_id):
    board = Board.query.get_or_404(board_id)

    request_body = request.get_json()
    if invalid_board_post_request_body(request_body):
        return make_response({"details": "Missing required data"}, 400)

    board.title = request_body["title"]
    board.owner = request_body["owner"]

    db.session.add(board)
    db.session.commit()

    return make_response(board.as_dict(), 200)


@boards_bp.route("/<int:board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = Board.query.get_or_404(board_id)

    db.session.delete(board)
    db.session.commit()
    return make_response(
        jsonify(
            details=f"board \"{board.title}\" successfully deleted", id=board.board_id),
        200)

# Handling CARDS


@boards_bp.route("/<int:board_id>/cards", methods=["GET"])
def get_rentals_by_board(board_id):
    board = Board.query.get_or_404(board_id)

    cards = [card.as_dict() for card in board.cards]

    return make_response(jsonify(cards), 200)


@boards_bp.route("/<int:board_id>/cards", methods=["POST"])
def create_card(board_id):
    request_body = request.get_json()

    if invalid_card_post_request_body(board_id, request_body):
        return make_response({"details": "Missing required data"}, 400)

    card = Card(message=request_body["message"], board_id=board_id)

    db.session.add(card)
    db.session.commit()

    return make_response({"id": card.card_id}, 201)


def invalid_card_post_request_body(board_id, request_body):
    board = Board.query.get(board_id)
    if ("message" not in request_body or board is None):
        return True
    return False


@boards_bp.route("/increase_likes/<int:card_id>", methods=["POST"])
def increase_likes(card_id):

    card = Card.query.get_or_404(card_id)

    card.likes_count += 1
    db.session.add(card)
    db.session.commit()

    return make_response({"id": card.card_id}, 201)


@boards_bp.route("/decrease_likes/<int:card_id>", methods=["POST"])
def decrease_likes(card_id):

    card = Card.query.get_or_404(card_id)

    card.likes_count -= 1
    db.session.add(card)
    db.session.commit()

    return make_response({"id": card.card_id}, 201)


@boards_bp.route("/delete_card/<int:card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)

    db.session.delete(card)
    db.session.commit()
    return make_response(
        jsonify(
            details="card \"{card.message}\" successfully deleted", id=card.card_id),
        200)
