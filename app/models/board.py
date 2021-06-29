from app import db
from app.models.card import Card
class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    
    cards = db.relationship("Card", lazy=True, cascade="all, delete")


    def as_dict(self):
        return {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,
        }

    def as_dict_with_cards(self):
        return {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,
            "cards": [card.as_dict() for card in self.cards]
        }
