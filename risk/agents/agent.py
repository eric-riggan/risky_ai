from abc import ABC, abstractmethod


class Agent(ABC):
    # return: name of the territory to be reinforced
    #@abstractmethod
    def reinforce_owned_territory(self, state):
        pass

    def reinforce_neutral_territory(self, state):
        pass
    # return: <to>, <from>, <troop_count>
    # <to> which territory to fortify
    # <from> which neighboring territory
    # <troop_count> with how many troops
    #@abstractmethod
    def fortify_territory(self, state):
        pass

    # return: 1 or 2 (number of troops committed to defend attacked_territory)
    #@abstractmethod
    def defend_territory(self, state, attacked_territory):
        pass

    # return: boolean, whether the agent wants to attack or not
    #@abstractmethod
    def wants_to_attack(self, state):
        pass

    # return: territory, attack source
    #@abstractmethod
    def select_attack_source(self, state):
        pass

    # return: territory, attack target
    #@abstractmethod
    def select_attack_target(self, state, source):
        pass

    # return: integer, troops involved in attack
    #@abstractmethod
    def select_attack_count(self, state, source):
        pass

    # return: boolean, whether the agent wants to fortify or not
    #@abstractmethod
    def wants_to_fortify(self, state):
        pass

    # return: territory, fortify source
    #@abstractmethod
    def select_fortify_source(self, state, target):
        pass

    # return: territory, fortify target
    #@abstractmethod
    def select_fortify_target(self, state):
        pass

    # return: integer, troops involved in fortification
    #@abstractmethod
    def select_fortify_count(self, state, source):
        pass
