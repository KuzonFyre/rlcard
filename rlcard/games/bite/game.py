import random
# TODO, identify order to which to process played cards. For Example, defensive cards and cards like Stake
# player damage and stake queue?
from rlcard.games.bite import Deck
from rlcard.games.bite import Round
from rlcard.games.bite import Player


class Game:


    def init_game(self):
        ''' Initialize the game

        Returns:
            (int): the current player's id
        '''
        self.deck = Deck()
        self.round = Round()
        self.players = [Player("vampire", 0), Player("human", 1), Player("human", 2),Player("vampire", 3), Player("human", 4)]
        self.deck.shuffle()
        self.current_player = 0
        return self.get_state(self.current_player), self.current_player
    def configure(self, game_config):
        ''' Specifiy some game specific parameters, such as number of players
        '''
        self.num_players = game_config['game_num_players']
    @staticmethod
    def get_num_actions():
        ''' Return the number of applicable actions

        Returns:
            number_of_actions (int): there are only two actions (hit and stand)
        '''
        return 141
    def draw_Three(self):
        return self.deck.draw(3)

    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            state (dict): corresponding player's state
        '''
        '''
                before change state only have two keys (action, state)
                but now have more than 4 keys (action, state, player0 hand, player1 hand, ... , dealer hand)
                Although key 'state' have duplicated information with key 'player hand' and 'dealer hand', I couldn't remove it because of other codes
                To remove it, we need to change dqn agent too in my opinion
                '''
        self.draws = self.draw_Three()

        actions = []
        for draw in self.draws:
            for j in range(1,6):
                actions.append(draw.id*j)

        state = self.players[player_id].get_state(actions,self.draws)
        for i in range(5):
            if i != player_id:
                state['player_' + str(i) + '_damage'] = self.players[i].damage
                state['player_' + str(i) + '_biteTokens'] = self.players[i].biteTokens
                state['player_' + str(i) + '_isBitten'] = self.players[i].isBitten
                state['player_' + str(i) + '_isCursed'] = self.players[i].isCursed
                # if self.players[player_id].role == "vampire" and self.players[i].role=="vampire":
                #     state['player_' + str(i) + 'role'] = self.players[i].role
        state['current_player'] = player_id

        return state


    def get_legal_actions(self):
        return self.players[self.current_player].get_legal_actions()

    def step(self, action):
        card = None
        playedIdx = None
        for draw in self.draws:
            if draw.id % action == 0 and (draw.id // action) <= 5:
                playedIdx = (draw.id // action) -1
                card = draw
            elif action % draw.id == 0 and (action // draw.id) <= 5:
                playedIdx = (action // draw.id) -1
                card = draw
            else:
                self.deck.discards.append(draw)
        played = self.players[playedIdx]
        self.round.roundQueue.append((card, self.players[self.current_player], played))
        if self.current_player == 4:
            for (card,player, played) in self.round.roundQueue:
                self.round.process_round(player, played,card)
                self.deck.discards.append(card)
            self.round.roundQueue = []
            self.current_player = 0
        else:
            self.current_player += 1
        return self.get_state(self.current_player), self.current_player



    def get_num_players(self):
        ''' Return the number of players in blackjack

        Returns:
            number_of_player (int): blackjack only have 1 player
        '''
        return self.num_players


    def get_player_id(self):
        ''' Return the current player's id

        Returns:
            player_id (int): current player's id
        '''
        return self.current_player
    def getIndex(self,prompt, lo, hi):
        while True:
            index = int(input(prompt))
            if lo <= index <= hi:
                return index
            else:
                print("Index out of range")
    def get_payoffs(self,playerIndex):

        if self.players[playerIndex].role == "vampire" and self.players[playerIndex].isAlive:
            return 1 + self.players[playerIndex].kills
        elif self.players[playerIndex].role == "human" and self.players[playerIndex].isAlive:
            return 1


    def is_over(self):
        ''' Check if the game is over

        Returns:
            (bool): True if the game is over, False otherwise
        '''
        for player in self.players:

            if not player.isAlive: return True
            return False