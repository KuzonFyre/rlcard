class HumanAgent(object):
    def __init__(self, num_actions):
        ''' Initilize the human agent

        Args:
            num_actions (int): the size of the output action space
        '''
        self.use_raw = True
        self.num_actions = num_actions
    @staticmethod
    def step(state):
        ''' Human agent will display the state and make decisions through interfaces

        Args:
            state (dict): A dictionary that represents the current state

        Returns:
            action (int): The action decided by human
        '''
        _print_state(state['raw_obs'], state['raw_legal_actions'],state['action_record'],state['hand'])
        action = int(input('>> You choose action (integer): '))
        played = int(input('>> You choose player to play on (integer): '))
        while action < 0 or action >= len(state['hand']):
            print('Action illegel...')
            action = int(input('>> Re-choose action (integer): '))
        return state['hand'][action], played

    def eval_step(self, state):
        ''' Predict the action given the curent state for evaluation. The same to step here.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
        '''
        return self.step(state), {}

def _print_state(state, raw_legal_actions, action_record,hand):
    ''' Print out the state

    Args:
        state (dict): A dictionary of the raw state
        action_record (list): A list of the each player's historical actions
    '''
    _action_list = []

    for i in range(1, len(action_record)+1):
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print('>> Player', pair[0], 'chooses', pair[1])

    print('\n=============   First Hand   ===============')
    print_card(hand)

    num_players = 5

    # for i in range(num_players):
    #     print('===============   Second Hand   ==============='.format(i))
    #     print_card(state['hand2'])
    print(raw_legal_actions)
    print('\n=========== Actions You Can Choose ===========')
    for(index, action) in enumerate(hand):
        print(index, ':', action)
    print('\n=========== Players to play on ===========')
    for i in range(num_players):
        print('Player', i)
        # print('Player', i, ':', state['players'][i])
    # print(', '.join([str(index) + ': ' + ', '.join(action) for index, action in enumerate(raw_legal_actions)]))
    print('')

def print_card(card):
    ''' Print out the card

    Args:
        card (list): A list of card
    '''
    if len(card) == 0:
        print('None')
    else:
        for c in card:
            print(c, end=' ')
    print('')