'''
Author: Hamilton Hardy
Date created: 3/24/2023
'''

import numpy as np
from collections import OrderedDict

from rlcard.envs import Env
from rlcard.games.bite import Game

DEFAULT_GAME_CONFIG = {
    'game_num_players': 5,
    'game_num_types': 28
}


class BiteEnv(Env):
    ''' Bite Environment
    '''

    def __init__(self, config):
        ''' Initialize the Bite environment
        '''
        self.game = Game()
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.name = 'bite'
        super().__init__(config)

        # self.default_game_config = DEFAULT_GAME_CONFIG
        self.num_types = 28
        self.actions = set()
        set_of_3 = [(card, player) for card in range(28) for player in range(self.num_players)]
        for action in set_of_3:
            self.actions.add(action)

        # Possible actions for the set of 2 cards
        set_of_2 = [(card, player) for card in range(28) for player in range(self.num_players)]
        for action in set_of_2:
            self.actions.add(action)
        self.state_shape = [[20] for _ in range(self.num_players)]
        self.action_shape = [[self.num_types] for _ in range(self.num_players)]

    def _get_legal_actions(self):
        ''' Get all leagal actions

        Returns:
            encoded_action_list (list): return encoded legal action list (from str to int)
        '''
        encoded_action_list = []
        for i in range(len(self.actions)):
            encoded_action_list.append(i)
        return encoded_action_list

    def _extract_state(self, state):
        ''' Extract the state representation from state dictionary for agent

        Args:
            state (dict): Original state from the game

        Returns:
            observation (list): combine the player's score and dealer's observable score for observation
        '''
        cards = state['state']
        print(cards)
        extracted_state = {}
        legal_actions = OrderedDict({i: None for i in range(len(self.actions))})

        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [a for a in self.actions]
        extracted_state['action_record'] = self.action_recorder
        extracted_state['hand'] = state['hand']
        return extracted_state

    def get_payoffs(self):
        ''' Get the payoff of a game

        Returns:
           payoffs (list): list of payoffs
        '''
        payoffs = []

        for i in range(self.num_players):
            self.game.get_payoffs(i)
            payoffs.append(self.game.get_payoffs(i))

        return np.array(payoffs)

    def _decode_action(self, action):
        ''' Decode the action for applying to the game

        Args:
            action id (int): action id

        Returns:
            action (str): action for the game
        '''
        return action
