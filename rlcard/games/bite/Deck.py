import random
from Card import Card
import json


class Deck:
    def __init__(self):
        self.discards = []
        with open("deck.json") as f:
            data = json.load(f)
            self.deck = []
            for item in data["items"]:
                self.deck.extend(
                    [Card(item["name"], item["quantity"], item["description"], item["type"],item["id"]) for _ in
                     range(item["quantity"])])
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def reset(self):
        self.deck.extend(self.discards)
        self.shuffle()
        self.discards = []

    def deal(self):
        if len(self.deck) == 0:
            self.reset()
            return self.deck.pop()
        else:
            return self.deck.pop()

    def __getitem__(self, item):
        return self.deck[item]

    def __setitem__(self, key, value):
        self.deck[key] = value

    def __len__(self):
        return len(self.deck)

    def __str__(self):
        st = ""
        for card in self.deck:
            st += str(card) + "\n"
        return st
