import numpy as np
generator = np.random.PCG64()
randomizer = np.random.Generator(generator)

class Game:
    verbose : bool
    def __init__(self, state, verbose=None):
        self.over = False
        self.state = state
        self.starter = None
        self.winner = None
        self.starting_players = len(state.players)
        self.turn_count = 0
        self.complete_round_count = 0
        self.verbose = False
        if verbose is None or verbose is False:
            self.verbose = False
            self.state.verbose = False
        elif verbose is True:
            self.verbose = True
            self.state.verbose = True
            self.state.board.verbose = True
            for player in self.state.players:
                player.verbose = True
            for terr in self.state.board.territories:
                self.state.board.territories[terr].verbose = True

    @staticmethod
    def roll_die(n):
        return randomizer.integers(
            low=1,
            high=6,
            endpoint=True,
            size=n
        ).tolist()
    
    @staticmethod
    def sort_2(l):
        '''
        Sorts a list of size n = 2
        '''
        if l[0] < l[1]:
            return [l[i] for i in [1, 0]]
        else:
            return l

    @staticmethod
    def sort_3(l):
        '''
        Sorts a list of size n = 3
        '''
        if l[0] < l[1]:
            if l[1] < l[2]:
                return [l[i] for i in [2, 1, 0]]
            elif l[0] < l[2]:
                return [l[i] for i in [1, 2, 0]]
            else:
                return [l[i] for i in [1, 0, 2]]
        elif l[1] < l[2]:
            if l[0] < l[2]:
                return [l[i] for i in [2, 0, 1]]
            else:
                return [l[i] for i in [0, 2, 1]]
        else:
            return l
    @staticmethod
    def dice_sort(l):
        if len(l) == 2:
            l = Game.sort_2(l)
        elif len(l) == 3:
            l = Game.sort_3(l)
        return l

    @staticmethod
    def resolve_attack(atk_str, def_str):
        # get number of dice to roll for each side
        atk_loss = 0
        def_loss = 0
        if atk_str > 0 and def_str > 0:
            if atk_str >= 3:
                atk_dice = 3
            if atk_str == 2:
                atk_dice = 2
            if atk_str == 1:
                atk_dice = 1
            if def_str >= 2:
                def_dice = 2
            if def_str == 1:
                def_dice = 1
        rolls = list(
            zip(
                Game.dice_sort(Game.roll_die(atk_dice)),
                Game.dice_sort(Game.roll_die(def_dice))
            )
        )
        for roll in rolls:
            # print(f'Attacker rolls: {roll[0]}. Defender rolls: {roll[1]}')
            if roll[0] > roll[1]:
                def_loss += 1
            else:
                atk_loss += 1
        # print(f'Attacker loses {atk_loss}. Defender loses {def_loss}.')
        return [atk_loss, def_loss]

    def find_winner(self):
        # for player in self.state.players:
        #     owned_terr_count = len(player.list_owned_territories(self.state))
        #     print(player.name, owned_terr_count)
        #     if owned_terr_count == 0:
        #         self.state.players.remove(player)
        # if len(self.state.players) == 1:
        #     print('GAME OVER!!')
        #     self.over = True
        #     self.winner = self.state.players[0].name
        # else:
        #     self.over = False
        # print(self.over)
        player_terrs = {}
        for player in self.state.players:
            owned_terr_count = len(player.list_owned_territories(self.state))
            player_terrs[player] = owned_terr_count
        for k, v in player_terrs.items():
            if v == 0:
                # player_to_remove = self.state.players.index[k]
                print(f'{k} has been eliminated.')
                # input('Press any key to continue...')
                self.state.players.remove(k)
                self.state.turn_order.remove(k)
        players_remaining = len(self.state.players)
        if players_remaining == 1:
            if self.verbose is True:
                print(f'Game over! Winner: {self.state.players[0].name}')
            self.winner = self.state.players[0].name
            print(self.complete_round_count, self.turn_count)
            return True
        else:
            return False

    def increment_turns(self):
        self.turn_count += 1
        self.complete_round_count = self.turn_count // self.starting_players
    
    def play_game(self):
        is_over = self.find_winner()
        while is_over is False:
            is_over = self.find_winner()
            if is_over is True:
                exit()
            self.increment_turns()
            self.state.turn_order[0].take_turn(self.state)
            self.state.turn_order.append(self.state.turn_order.pop(0))
