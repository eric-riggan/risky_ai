class Continent:
    """
    A collection of territories.
    At the beginning of each player's turn, if they own
    all Territories in a Continent, that player is awarded
    additional armies to place during the Draft phase
    equal to the Supply Bonus for the Continent.

    Attributes
    ----------
    name : str
        Name of Continent
    territories : list
        List of Territory classes belonging to the Continent
    supply_bonus : int
        Bonus armies awarded to the Continent Owner during the Draft phase

    Methods
    -------
    add_territory(territory):
        Adds a Territory class to the Continent
    get_owner():
        Returns the Player who owns the Continent (if any)
    """
    def __init__(self, name, territories, supply_bonus):
        self.name = name
        self.territories = territories
        self.supply_bonus = supply_bonus

    def add_territory(self, territory):
        """
        Used in board creation. Adds territory classes to the Continent class.

        Keyword arguments:
        self -- the Continent
        territory -- the territory class to add
        """
        self.territories.append(territory)

    def __str__(self) :
        return f'{self.name} - Supply bonus: {self.supply_bonus}. Territories: \n {self.territories}' + '\n'

    def get_owner(self):
        """
        If the entire continent is owned by one player, get the player.
        self -- the Continent
        """
        owners = set()
        for territory in self.territories:
            owners.add(territory.owner)

        if len(owners) == 1:
            return owners.pop()
        else:
            return None
