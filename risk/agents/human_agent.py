from risk.agents.agent import Agent
from risk.utils.game_exceptions import (
    CannotAttackTerritoryException,
    CannotCommitUnitCount,
    TerritoryDoesNotExistException,
    InvalidInputException
)
class HumanAgent(Agent):

    # overriding abstract method
    # reinforce_owned_territory()
    def reinforce_owned_territory(self, state):
        valid_input = False
        while valid_input is False:
            try:
                territory_name = input('Reinforce owned territory: ').strip()
                if territory_name in state.board.territories:
                    valid_input = True
                else:
                    raise TerritoryDoesNotExistException()
            except TerritoryDoesNotExistException:
                print(f'{territory_name} does not exist. Try again.')
        return state.board.territories[territory_name]
    
    def reinforce_neutral_territory(self, state):
        territory_name = input('Reinforce neutral territory: ').strip()
        return state.board.territories[territory_name]
    
    def wants_to_attack(self, state):
        to_attack = None
        while to_attack is None:
            try:
                wants_to_attack = input('Do you want to attack? (Y / N): ').strip()
                if wants_to_attack == 'Y':
                    to_attack = True
                elif wants_to_attack == 'N':
                    to_attack = False
                else:
                    raise InvalidInputException()
            except InvalidInputException:
                print(f'Input was not "Y" or "N". Try again.')
        return to_attack
    
    def defend_territory(self, state, attacked_territory):
        valid_input = False
        while valid_input is False:
            try:
                units = input(f'How many units to defend with? (max {min(attacked_territory.strength, 2)}): ')
                units = int(units)
                if units <= attacked_territory.strength:
                    valid_input = True
                else:
                    raise CannotCommitUnitCount()
            except CannotCommitUnitCount:
                print(f'Cannot commit {units} units - max is {attacked_territory.strength}. Try again.')
            except ValueError:
                print('Not an integer. Try again.')
        return units
    
    def occupy(self, source, target, unit_count):
        valid_input = False
        while valid_input is False:
            try:
                print(f'{source} has conquored {target}!')
                units = input(f'How many units to occupy with? (min {unit_count}, {source.strength - 1} available): ').strip()
                units = int(units)
                if units >= unit_count and units < source.strength:
                    valid_input = True
                else: 
                    raise CannotCommitUnitCount()
            except CannotCommitUnitCount:
                print(f'{units} must be at least {unit_count} and less than {source.strength}. Try again.')
            except ValueError:
                print('Not an integer. Try again.')
        return units
    
    def select_attack_source(self, state):
        valid_input = False
        while valid_input is False:
            try:
                terr_name = input('Attack a territory to attack from: ').strip()
                if terr_name in state.board.territories:
                    valid_input = True
                else:
                    raise CannotAttackTerritoryException()
            except CannotAttackTerritoryException:
                print(f'{terr_name} does not exist. Try again.')
        return state.board.territories[terr_name]
    
    def select_attack_target(self, state, source):
        valid_input = False
        while valid_input is False:
            try:
                terr_name = input(f'Select territory to attack from {source}: ')
                print(source.name)
                legal_attacks = [terr.name for terr in state.board.territories[terr_name].can_be_attacked_from()]
                if source.name in legal_attacks:
                    valid_input = True
                else:
                    raise CannotAttackTerritoryException()
            except CannotAttackTerritoryException:
                print(f'{terr_name} is not a legal target. Try again')
        return state.board.territories[terr_name]
    
    def select_attack_count(self, state, source):
        valid_input = False
        max_units = min(source.strength, 3)
        while valid_input is False:
            try:
                units = input(f'How many units to attack with? (max: {max_units}): ').strip()
                units = int(units)
                if units > 0 and units <= max_units:
                    valid_input = True
                else:
                    raise CannotCommitUnitCount()
            except CannotCommitUnitCount:
                print(f'Cannot commit {units} to attack. Must be between 1 and {max_units}')
            except ValueError:
                print('Not an integer. Try again.')
        return units
