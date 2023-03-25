import random
from rlcard.games.bite import Card
import json
import os
import rlcard

class Deck:
    def __init__(self):
        self.discards = []
        with open(os.path.join(rlcard.__path__[0], 'games/bite/deck.json'), 'r') as f:
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
        self.deck = self.discards
        self.shuffle()
        self.discards = []

    def draw(self, num=1):
        if len(self.deck) == 0:
            self.reset()
        li = []
        for i in range(num):
            if len(self.deck) == 0:
                print(self.discards)
                self.reset()
            li.append(self.deck.pop())
        return li

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
