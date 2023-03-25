from Bite import Bite
import random
import gymnasium as gym
import rlcard
from rlcard.agents import RandomAgent
from enum import Enum

b = Bite()
# class BiteEnv(rlcard.envs.Env):


class BiteRound:
# for player in b.players:
#     print("Player Options: ")
#     player.cycle_hand(b.draw())
#     for card in player.hand:
#         print(card)
#         b.processFactory(player, random.choice(b.players), card)

# for player in b.players:
#     print(player, end="\n\n")

    def proceed_round(self, player, played, card):
            if card.type == "instant":
                self.processInstant(player, played, card)
            elif card.type == "keep down":
                self.processKeepDown(player, played, card)
            elif card.type == "keep up":
                self.processKeepUp(player, played, card)
            self.deck.discards.append(card)

    def processKeepDown(self, player, played, card):
        print()

    def processKeepUp(self, player, played, card):
        print()

    def processInstant(self, player, played, card):
        if card.name == "bite":
            played.isBitten = True
        elif card.name == "wound":
            played.damage += 1
        elif card.name == "revolver":
            toWound = self.players[self.getIndex("Who do you want to play this on?", 0, len(self.players) - 1)]
            toWound.damage += 1
        elif card.name == "Stake":
            # TODO: Account for order of play
            played.damage += 1
        elif card.name == "Turn":
            if played.isBitten:
                player.role = "vampire"
        elif card.name == "hallowed ground":
            for p in self.players:
                self.discardFaceDown(p)
        elif card.name == "cured":
            if played.role == "vampire":
                # TODO: Add played to a public roles list
                played.role = "human"
        elif card.name == "garlic":
            print()
    #         TODO: Bite Prevention
        elif card.name == "terror":
            print()
    #         TODO: No defense
        elif card.name == "peace":
            for p in self.players:
                choice = self.getIndex(f"Choose 0 to remove a bite token and 1 to remove a wound token. You have {p.biteTokens} bite tokens and {p.damage} wound tokens.", 0, 1)
                if choice == 0 and p.biteTokens > 0:
                    p.biteTokens -= 1
                elif choice == 1 and p.damage > 0:
                    p.damage -= 1
        elif card.name == "torch":
            self.discardFaceDown(played)


    def discardFaceDown(self,player):
            if player.faceDownCards:
                self.getIndex("What face down card do you want to discard?", 0, len(player.faceDownCards)-1)
