# from risk.agents.agent import Agent
import numpy as np
# generator = np.random.PCG64()
# self.randomizer = np.random.Generator(generator)

class NaiveAgent():

    def __init__(self):
        self.randomizer = np.random.Generator(np.random.PCG64())

    def reinforce_owned_territory(self, state):
        # print('reinforce_owned_territory')
        # print(state.turn_order[0].name)
        territories = state.board.owned_territories(state.turn_order[0])
        if len(territories) > 1:
            territory = self.randomizer.choice(territories, size=1)[0]
        else:
            territory = territories[0]
        return territory
    
    def reinforce_neutral_territory(self, state):
        # print('reinforce_neutral_territory')
        territories = state.board.unowned_territories()
        territory = self.randomizer.choice(territories, size=1)[0]
        return territory
    
    def wants_to_attack(self, state):
        if len(state.board.legal_attacks(state.turn_order[0])) > 0:
            return True
        else:
            return False
        # return self.randomizer.choice([True, False], size=1)[0]
    
    def select_attack_source(self, state):
        # print('select_attack_source')
        territories = state.board.legal_attacks(state.turn_order[0])
        territory = self.randomizer.choice(territories, size=1)[0]
        return territory
    
    def select_attack_target(self, state, source):
        # print('select_attack_target')
        enemy_neighbors = source.enemy_neighbors()
        target = self.randomizer.choice(enemy_neighbors, size=1)[0]
        return target
    
    def select_attack_count(self, state, source):
        # print('select_attack_count')
        units = min(max(source.strength - 1, 1), 3)
        return units
    
    def defend_territory(self, state, attacked_territory):
        # print('defend')
        units = min(attacked_territory.strength, 2)
        return units
    
    def occupy(self, source, target, unit_count):
        print(f'{source} has conquored {target}!')
        high = source.strength - 1
        low = low = min(unit_count, high)
        # print(f'low={low},high={high}')
        units = self.randomizer.integers(
            low=low,
            high=source.strength -1,
            endpoint=True,
            size=1
        ).tolist()[0]
        # print(units)
        return units