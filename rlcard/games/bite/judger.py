class BiteJudger():

    def judge(self):
        ''' Judge if the game is over

        Returns:
            (bool): If the game is over
        '''
        return self.game.round > self.game.max_round

    def judge_round(self, ):
        ''' Judge the target player's status

        Args:
            player (int): target player's id

        Returns:
            status (str): the status of the target player
            score (int): the current score of the player
        '''
        score = self.judge_score(player.hand)
        if score <= 21:
            return "alive", score
        else:
            return "bust", score
    def get_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (dict): The payoffs of the game
        '''
        payoffs = {}
        for player_id in range(self.game.player_num):
            payoffs[player_id] = self.game.players[player_id].score
        return payoffs