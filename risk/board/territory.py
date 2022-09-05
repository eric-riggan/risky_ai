class Territory:
    """
    A single territory object.
    The Risk board can be represented as Graph. In this paradigm,
    a Territory is a Node, while Borders form the Edges.
    Territories can be grouped together to form Continents.

    This object has several calculated attributes which require further
    explaination: Border Security Threat (BST), Border Security Ratio (BSR),
    and Normalized Border Security Ratio (NBSR)
    - Border Security Threat (BST)
        - The sum of the strength of all adjacent Territories owned by
        players that are not the owner of this Territory (enemy neighbors)
    - Border Security Ratio (BSR)
        - The ratio of this Territory's strength to it's BST
        - BSR = BST / strength
    - Normalized Border Security Ratio (NBSR)
        - This Territory's BSR divided by the BSR of all Territorys
        owned by the owner of this Territory - that is to say, all 
        friendly Territories.
        - NBSR = BSRx / SUM(BSRz)
            - where BSRx is this Territory and BSRz 

    Attributes
    ----------
    name : str
        Name of Territory
    neighbors : list
        The list of other Territories this Territory
        is adjacent to.
    owner : Class
        The Player who currently controls the Territory.
        Defaults to None (the game begins with an empty board)
    strength : int
        The number of units currently occupying the Territory.
    nbsr : float
        Defaults to zero, is recalculated after every action which
        modifies the strength of the territory.
    verbose : bool
        When set to True, allows various attributes to print to terminal.

    Properties
    ----------
    bst():
        Border Security Threat:
            The sum of the strength of all adjacent 
            Territories owned by players that are not the owner of this
            Territory (enemy neighbors)

    bsr():
        Border Security Ratio:
            - The ratio of this Territory's strength to it's BST
            - BSR = BST / strength

    Methods
    -------

    add_neighbor(neighbor):
        Adds a Territory as an adjacent territory to this one.

    is_border_territory():
        Returns True if any adjacent Territories are owned by Players
        other than the owner of this Territory

    enemy_neighbors():
        Returns a list of all adjacent Territories
        owned by Players other than the owner of this Territory

    fortify_sources()
        Returns a list of adjacent Territories meeting the following conditions:
        1. Is owned by the same owner as this Territory (i.e. is friendly)
        2. Has more than one unit on it

    modify_strength():
        Adjusts this Territory's Strength, then recalculates it's BSR and BST

    can_be_attack_source():
        Returns True if the following conditions are met:
        1. Any adjacent Territory is owned by a player other than this
            this Territory's owner
        2. This Territory's strength is greater than one.
    """
    verbose: bool
    def __init__(self, name, verbose=None):
        self.name = name
        self.neighbors = []
        self.owner = None
        self.strength = 0
        self.nbsr = 0
        if verbose is None or verbose is False:
            self.verbose = False
        if verbose is True:
            self.verbose = True

    def __str__(self):
        return self.name

    @property
    def bst(self):
        """
        Border Security Threat:
            The sum of the strength of all adjacent 
            Territories owned by players that are not the owner of this
            Territory (enemy neighbors)
        """
        bst = sum([enemy.strength for enemy in self.enemy_neighbors()])
        return bst

    @property
    def bsr(self):
        """
        Border Security Ratio:
            - The ratio of this Territory's strength to it's BST
            - BSR = BST / strength
        """
        bst = sum([enemy.strength for enemy in self.enemy_neighbors()])
        bsr = bst / self.strength
        return bsr

    def add_neighbor(self, neighbor):
        """
        Adds a Territory to the neighbors attribute of this Territory.
        Fails silently if an attempt is made to make a Territory
        it's own neighbor.
        Keyword arguments:
        neighbor -- another Territory class to add.
        """
        if neighbor != self:
            self.neighbors.append(neighbor)

    def is_border_territory(self):
        """
        Checks all adjacent Territories to see if they
        are owned by the owner of this Territory
        """
        for neighbor in self.neighbors:
            if neighbor.owner != self.owner:
                return True
        return False

    def enemy_neighbors(self):
        """
        Returns a list of all adjacent Territories
        owned by Players other than the owner of this Territory
        """
        enemy_neighbors = []
        for neighbor in self.neighbors:
            if neighbor.owner != self.owner:
                enemy_neighbors.append(neighbor)
        return enemy_neighbors

    def fortify_sources(self):
        """
        Returns a list of adjacent Territories meeting the following conditions:
        1. Is owned by the same owner as this Territory (i.e. is friendly)
        2. Has more than one unit on it
        """
        fortify_sources = []
        for neighbor in self.neighbors:
            if neighbor.strength > 1 and neighbor.owner == self.owner:
                fortify_sources.append(neighbor)

    def can_be_attack_source(self):
        """
        Returns True if the following conditions are met:
        1. Any adjacent Territory is owned by a player other than this
            this Territory's owner
        2. This Territory's strength is greater than one.
        """
        for neighbor in self.neighbors:
            if neighbor.owner != self.owner and self.strength > 1:
                return True
        return False
    
    def can_be_attacked_from(self):
        attack_sources = []
        for neighbor in self.enemy_neighbors():
            if neighbor.strength > 1:
                attack_sources.append(neighbor)
        return attack_sources

    def modify_strength(self, modifier):
        """
        Adjusts this Territory's Strength, then recalculates it's BSR and BST

        Keyword arguments:
        modifier -- signed integer to adjust this object's Strength by.
        """
        self.strength += modifier
        if self.verbose is True:
            print(f'{self.name}: {self.strength} units.')
