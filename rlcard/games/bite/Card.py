import json


class Card:
    def __init__(self, name, quantity, description, card_type,cid):
        self.name = name
        self.quantity = quantity
        self.description = description
        self.type = card_type
        self.id = cid
    def __str__(self):
        return f"{self.name} ({self.type}): {self.description} ({self.quantity})"



