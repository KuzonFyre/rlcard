

# class BiteEnv(rlcard.envs.Env):


class Round:
    def __init__(self):
        self.roundQueue = []

    def process_round(self, player, played, card):
            if card.type == "instant":
                self.processInstant(player, played, card)
            elif card.type == "keep down":
                self.processKeepDown(player, played, card)
            elif card.type == "keep up":
                self.processKeepUp(player, played, card)
            if played.role == "human" and played.damage >= 3:
                if player.role == "vampire":
                    player.kills = player.kills + 1
                else:
                    player.kills = player.kills - 1
            if played.role == "vampire" and played.damage >= 3:
                if player.role == "human":
                    player.kills = player.kills + 1
                else:
                    player.kills = player.kills - 1
                played.isAlive = False



    def processKeepDown(self, player, played, card):
        if card.name == "padding":
            played.faceDownCards.append(card)
        elif card.name == "bible":
            played.faceDownCards.append(card)
        elif card.name == "cross":
            played.faceDownCards.append(card)
        elif card.name == "mist form":
            played.faceDownCards.append(card)
    def processKeepUp(self, player, played, card):
        print()
    #
    # def get_legal_actions(self):
    #     print()
    def processInstant(self, player, played, card):
        if card.name == "dodge":
            played.faceDownCards.append(card)
        elif card.name == "bite":
            for x in played.faceDownCards:
                if x.name == "garlic":
                    played.faceDownCards.remove(x)
                    break
                elif x.name == "cross":
                    played.faceDownCards.remove(x)
                    break
                else:
                    played.isBitten = True
        elif card.name == "wound":
            for x in played.faceDownCards:
                if x.name == "padding":
                    played.faceDownCards.remove(x)
                    break
                elif x.name == "bible":
                    played.faceDownCards.remove(x)
                    break
                elif x.name == "cross":
                    played.faceDownCards.remove(x)
                    break
                else:
                    played.damage += 1
        elif card.name == "Stake":
            for x in played.faceDownCards:
                if x.name == "mist form":
                    played.faceDownCards.remove(x)
                else:
                    played.damage += 1
        elif card.name == "turned":
            if played.isBitten:
                player.role = "vampire"
        elif card.name == "hallowed ground":
            if player.faceDownCards:
                player.faceDownCards.pop()
            if played.faceDownCards:
                played.faceDownCards.pop()
        elif card.name == "cured":
            if played.role == "vampire":
                # TODO: Add played to a public roles list
                played.role = "human"
        elif card.name == "cursed":
            played.isCursed = True
        elif card.name == "heal":
            if not played.isCursed:
                played.damage -= 1
    # #         TODO: Bite Prevention
        elif card.name == "holy water":
            if played.role == "vampire":
                played.roleRevealed = True
        elif card.name == "torch":
            if played.faceDownCards != []:
                played.faceDownCards.pop()
        elif card.name == "peace":
            played.damage -= 1
            player.damage -= 1
        elif card.name == "suspicion":
            played.suspicion += 1
            if played.suspicion >= 3:
                played.roleRevealed = True

        for x in played.faceDownCards:
            if x.name == "dodge":
                played.faceDownCards.remove(x)
