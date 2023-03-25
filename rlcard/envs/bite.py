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

        self.actions = []
        for i in range(self.num_types * self.num_players + 1):
            self.actions.append(i)
        self.state_shape = [[20] for _ in range(self.num_players)]
        self.action_shape = [[self.num_types] for _ in range(self.num_players)]

    def _get_legal_actions(self):
        ''' Get all leagal actions

        Returns:
            encoded_action_list (list): return encoded legal action list (from str to int)
        '''
        encoded_action_list = []
        for i in range(len(self.action_shape)):
            encoded_action_list.append(i)
        return encoded_action_list

    def _extract_state(self, state):
        ''' Extract the state representation from state dictionary for agent

        Args:
            state (dict): Original state from the game

        Returns:
            observation (list): combine the player's score and dealer's observable score for observation
        '''
        extracted_state = {}
        self.legal_actions = OrderedDict({self.actions.index(a): None for a in state['legal_actions']})
        extracted_state['legal_actions'] = self.legal_actions
        obs = np.zeros(20)
        obs[0] = int(state['damage'])
        obs[1] = int(state['isBitten'])
        obs[2] = int(state['isCursed'])
        # obs[3] = int(len(state['faceDownCards']))
        # obs[4] = int(len(state['faceUpCards']))
        obs[3] = int(state['biteTokens'])
        if state['role'] == 'vampire':
            obs[4] = 1
        elif state['role'] == 'human':
            obs[4] = 2
        i=0
        for j in range(0,5):
            if j != state['current_player']:
                obs[5+i] = int(state['player_'+ str(j) + "_damage"])
                obs[6+i] = int(state['player_'+ str(j) + "_biteTokens"])
                obs[7+i] = int(state['player_'+ str(j) + "_isBitten"])
                if i+8 == 20:
                    break
                obs[8+i] = int(state['player_'+ str(j) + "_isCursed"])
                # obs[11+i] = int(len(state['player_'+ str(j) + "_faceDownCards"]))
                # obs[12+i] = int(len(state['player_'+ str(j) + "_faceUpCards"]))
                i+=4
        extracted_state['obs'] = obs
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [a for a in state['legal_actions']]
        extracted_state['action_record'] = self.action_recorder
        return extracted_state

    def get_payoffs(self):
        ''' Get the payoff of a game

        Returns:
           payoffs (list): list of payoffs
        '''
        payoffs = []

        for i in range(self.num_players):
            payoffs.append(self.game.get_payoffs(i))

        return np.array(payoffs)

    def _decode_action(self, action):
        ''' Decode the action for applying to the game

        Args:
            action id (int): action id

        Returns:
            action
        '''

        return action
