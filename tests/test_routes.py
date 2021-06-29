from app.models.board import Board


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