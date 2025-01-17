import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def one_board(app):
    new_board = Board(
        title="hi baker!", owner="hi tomilho!")
    db.session.add(new_board)
    db.session.commit()


@pytest.fixture
def one_board_with_cards(app):
    new_board = Board(
        title="hi baker!", owner="hi tomilho!")
    new_card = Card(
        message="Our pets are the best!",
        board_id=1
    )
    db.session.add(new_board)
    db.session.add(new_card)
    db.session.commit()


@pytest.fixture
def multi_boards_with_cards(app):
    db.session.add_all([
        Board(
            title="Baker is the best dog in the world", owner="Baker"),
        Board(
            title="Tomi is the best cat in the world", owner="Tomi"),
        Board(
            title="Jota is the best fish in the world", owner="Jota"),
        Card(
            message="Jpug is cool!", board_id=1),
        Card(
            message="Our pets are the best!", board_id=1),
        Card(
            message="Our pets are the best!", board_id=3)
    ])

    db.session.commit()
