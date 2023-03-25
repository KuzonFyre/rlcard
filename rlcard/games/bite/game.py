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
        # print(self.deck)
        self.players = [Player("vampire", 0), Player("human", 1), Player("human", 2),Player("vampire", 3), Player("human", 4)]
        self.deck.shuffle()
        # self.deck.deal(self.players)
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
        return 140
    def draw_Three(self):
        return [self.deck.deal(), self.deck.deal(), self.deck.deal()]

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
        state = {}
        actions = set()
        set_of_3 = [(card, player) for card in range(28) for player in range(5)]
        for action in set_of_3:
            actions.add(action)

        # Possible actions for the set of 2 cards
        set_of_2 = [(card, player) for card in range(28) for player in range(5)]
        for action in set_of_2:
            actions.add(action)
        state['actions'] = actions
        state['hand'] = self.draw_Three()
        # hand = [card.get_index() for card in self.players[player_id].hand]

        stat = self.players[player_id].get_state()

        state['state'] = stat

        return state

    def step(self, action):
        card, played = action
        self.round.roundQueue.append((card, self.players[self.current_player], self.players[played]))

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
    def is_over(self):
        ''' Check if the game is over

        Returns:
            (bool): True if the game is over, False otherwise
        '''
        for player in self.players:
            if player.damage == 4:
                return True
        return False