from risk.game.game import Game
from risk.utils.game_exceptions import *

class AIPlayer:
    verbose: bool
    def __init__(self, name, agent, verbose=None):
        self.name = name
        self.agent = agent
        self.unit_pool = 0
        if verbose is None or verbose is False:
            self.verbose = False
        if verbose is True:
            self.verbose = True
    
    def __str__(self):
        return self.name
    
    def list_owned_territories(self, state):
        terr_list = []
        for k, v in state.board.territories.items():
            if v.owner == self:
                terr_list.append(v)
        return terr_list

    def reinforce_owned_territory(self, state, unit_pool):
        units = unit_pool
        while units > 0:
            valid_response = False
            while valid_response is False:
                try:
                    territory = self.agent.reinforce_owned_territory(state)
                    if territory.owner == self:
                        valid_response = True
                        territory.modify_strength(1)
                        state.update_nbsr()
                        units -= 1
                    else:
                        raise TerritoryNotOwnedByPlayerException()
                except TerritoryNotOwnedByPlayerException:
                    if self.verbose is True:
                        print(f"You don't own {territory}. Try again.")
        self.unit_pool = 0


    def reinforce_neutral_territory(self, state):
        territory = self.agent.reinforce_neutral_territory(state)
        if territory.owner:
            raise TerritoryNotNeutralException()
        else:
            territory.modify_strength(1)
            state.update_nbsr()
    
    def receive_units(self, state):
        # Calculate reinforcement bonus from owned territories
        owned_terr_num = state.board.owned_territories(self)
        terr_bonus = max(len(owned_terr_num), 9) // 3
        
        # Get continent bonus
        owned_continents = state.board.owned_continents(self)
        continent_bonus = 0
        for continent in owned_continents:
            continent_bonus += continent.supply_bonus
        
        # placeholder for cards
        card_bonus = 0

        self.unit_pool = terr_bonus + continent_bonus + card_bonus
    
    def place_units(self, state):
        while self.unit_pool > 0:
            if self.verbose is True:
                print(f'{self.name} has {self.unit_pool} units to place.')
            self.reinforce_owned_territory(state, self.unit_pool)
            # self.unit_pool -= 1
    
    def wants_to_attack(self, state):
        return self.agent.wants_to_attack(state)
    
    def defend_territory(self, state, def_terr):
        units = self.agent.defend_territory(state, def_terr)
        return units
    
    def occupy(self, state, source, target, unit_count):
        units = self.agent.occupy(source, target, unit_count)
        units = max(unit_count, units)
        source.modify_strength(-units)
        target.modify_strength(units)
        if len(state.board.owned_territories(self)) != len(state.board.territories):
            state.update_nbsr()

    def attack(self, state):
        state.attack_succeeded = False

        # decide source attack territory
        legal_attack = False
        while legal_attack is False:
            try: 
                source = self.agent.select_attack_source(state)
                if source.owner != self:
                    raise TerritoryNotOwnedByPlayerException()
                elif source.can_be_attack_source() is False:
                    raise CannotAttackTerritoryException()
                else:
                    target = self.agent.select_attack_target(state, source)
                    if source in target.can_be_attacked_from():
                        legal_attack = True
                    else:
                        raise CannotAttackTerritoryException()
            except TerritoryNotOwnedByPlayerException:
                if self.verbose is True:
                    print(f"You don't control {source}. Try again")
            except CannotAttackTerritoryException:
                if self.verbose is True:
                    print(f"No legal attacks from {source}. Try again.")
        if self.verbose is True:
            print(f'{source} ({self.name}) attacks {target} ({target.owner.name})')
            print(f'{source}: {source.strength} vs {target}: {target.strength}')
        attack_str = self.agent.select_attack_count(state, source)
        defense_str = target.owner.defend_territory(state, target)
        atk_loss, def_loss = Game.resolve_attack(attack_str, defense_str)
        source.modify_strength(-atk_loss)
        target.modify_strength(-def_loss)
        if self.verbose is True:
            print(f'source strength: {source.strength}. target strength: {target.strength}')
        if target.strength > 0:
            state.update_nbsr()
        else:
            target.owner = self
            self.occupy(state, source, target, attack_str)
            state.attack_succeeded = True
            if len(state.board.territories) != len(state.board.owned_territories(self)):
                state.update_nbsr()
    

    def wants_to_fortify(self, state):
        return self.agent.wants_to_fortify(state)

    def take_turn(self, state):
        if self.verbose is True:
            print(f'{self.name}, it''s your turn!!')
        self.receive_units(state)
        self.place_units(state)
        source_terrs = state.board.legal_attacks(self)
        while source_terrs and self.wants_to_attack(state):
            self.attack(state)
            source_terrs = state.board.legal_attacks(self)