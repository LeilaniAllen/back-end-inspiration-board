from app.models.board import Board
from app.models.card import Card

def test_get_boards_no_boards(client):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def get_boards_one_board(client, one_board):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [{
        "board_id": 1,
        "title": "hi baker!",
        "owner": "hi tomilho!"
    }]


def get_board(client, one_board):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [{
        "board_id": 1,
        "title": "hi baker!",
        "owner": "hi tomilho!",
        "cards": []
    }]


def get_board_not_found(client):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None


def test_update_board(client, one_board):
    response = client.put("boards/1", json={
        "title": "updated title",
        "owner": "updated owner"
    })

    response_body = response.get_json()
    assert response.status_code == 200
    assert response_body == {"title": "updated title",
                             "owner": "updated owner",
                             "board_id": 1}


def test_delete_board(client, one_board):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "details": "board \"hi baker!\" successfully deleted", "id": 1
    }
    assert Board.query.get(1) == None


def test_delete_board_not_found(client):
    response = client.delete("/boards/3")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None


def test_delete_board_not_found_with_board(client, one_board):
    response = client.delete("/boards/8")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None

def test_create_card(client, one_board):
    response = client.post("/boards/1/cards", json={"message": "Baker and Tomi are friends!"})
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {"id": 1}
    assert Board.query.get(1).cards[0].as_dict() == {'card_id': 1, 'message': 'Baker and Tomi are friends!', 'likes_count': 0, 'board_id': 1}

def test_create_card_invalid_board(client, one_board):
    response = client.post("/boards/3/cards", json={"message": "Baker and Tomi are friends!"})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {'details': 'Missing required data'}
    

def test_increase_likes(client, one_board_with_cards):
    response = client.post("/boards/increase_likes/1")
    
    assert response.status_code == 200
    assert Card.query.get(1).likes_count == 1

def test_decrease_likes(client, one_board_with_cards):
    response = client.post("/boards/decrease_likes/1")
    
    assert response.status_code == 200
    assert Card.query.get(1).likes_count == -1

def test_delete_cards(client, one_board_with_cards):
    response = client.delete("/boards/delete_card/1")
    response_body = response.get_json()
    print(response_body)

    assert response.status_code == 200
    assert response_body == {
        "details": "card \"Our pets are the best!\" successfully deleted", "id": 1}
    assert Card.query.get(1) == None

