import numpy as np
import pandas as pd
generator = np.random.PCG64()
randomizer = np.random.Generator(generator)

class State:
    verbose : bool
    def __init__(self,board,players,deck, verbose=None):
        self.board = board
        self.players = players
        self.deck = deck
        self.turn_order = randomizer.choice(
            self.players,
            size=len(self.players),
            replace=False
        ).tolist()
        self.attack_succeeded = False
        if verbose is None or verbose is False:
            self.verbose = False
            self.board.verbose = False
            for player in self.players:
                player.verbose = False
        elif verbose is True:
            self.verbose = True
            self.board.verbose = True
            for player in self.players:
                player.verbose = True

    def update_nbsr(self):
        for player in self.players:
            terr_list = []
            for k, v in self.board.territories.items():
                if v.owner == player:
                    terr_list.append(v)
            for terr in terr_list:
                terr.nbsr = terr.bsr / sum([territory.bsr for territory in terr_list])

    def list_unowned_territories(self):
        terr_list = []
        for k, v in self.board.territories.items():
            if v.owner is None:
                terr_list.append(v)
        return terr_list

    def list_owned_territories(self, player):
        terr_list = []
        for k, v in self.board.territories.items():
            if v.owner == player:
                terr_list.append(v)
        return terr_list

    def select_random_unowned_territory(self):
        unowned_terrs = self.list_unowned_territories()
        random_terr = randomizer.choice(unowned_terrs, size=1, replace=False)[0]
        return random_terr

    def select_random_owned_territory(self, player):
        owned_terrs = self.list_owned_territories(player)
        random_terr = randomizer.choice(owned_terrs, size=1, replace=False)[0]
        return random_terr

    def random_start(self):
        army_pool = []
        player_count = len(self.players)
        if player_count == 3:
            starting_armies = 35
        elif player_count == 4:
            starting_armies = 30
        elif player_count == 5:
            starting_armies = 25
        elif player_count == 6:
            starting_armies = 20

        for player in self.players:
            army_pool.append({
                'player': player,
                'armies': starting_armies
            })

        army_pool_df = pd.DataFrame(
            army_pool
        )
        is_running = 1
        while is_running != 0:
            for player in self.turn_order:
                army_pool_df.loc[
                    army_pool_df['player'] == player, 'armies'
                ] = army_pool_df.loc[
                    army_pool_df['player'] == player, 'armies'
                ] - 1
                if len(self.list_unowned_territories()) != 0:
                    territory = self.select_random_unowned_territory()
                    territory.owner = player
                    territory.strength += 1
                else:
                    territory = self.select_random_owned_territory(player)
                    territory.strength += 1
                if army_pool_df['armies'].sum() == 0:
                    is_running = 0
