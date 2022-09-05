class TerritoryNotOwnedByPlayerException(Exception):
    pass

class TerritoryNotNeutralException(Exception):
    pass


class CannotAttackTerritoryException(Exception):
    pass

class CannotFortifyTerritoryException(Exception):
    pass

class CannotCommitUnitCount(Exception):
    pass

class TerritoryDoesNotExistException(Exception):
    pass

class InvalidInputException(Exception):
    pass