class Border:
    """
    Defines how Territory objects are connected to each other.
    If the Risk board can be represented as a Graph, Borders represent
    the edges of that graph.

    Attributes
    ----------
    source_territory : class (Territory)
        The starting point of the Border
    destination_territory : class (Territory)
        The finishing point of the Border
    """
    def __init__(self, source_territory, destination_territory):
        self.source_territory = source_territory
        self.destination_territory = destination_territory

    def __str__(self):
        return f'Border between {self.source_territory} and {self.destination_territory}'
