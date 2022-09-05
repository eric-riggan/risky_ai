# Import required third-party modules
import pyodbc
import pandas as pd
import networkx as nx

# Import Classes
from risk.board.border import Border
from risk.board.territory import Territory
from risk.board.continent import Continent

class Board:
    verbose: bool
    def __init__(self, territories, borders, continents, name, verbose=None):
        self.territories = territories
        self.borders = borders
        self.continents = continents
        self.name = name
        if verbose is None or verbose is False:
            self.verbose = False
            for territory in self.territories:
                self.territories[territory].verbose = False
        elif verbose is True:
            self.verbose = True
            for territory in self.territories:
                territory.verbose = True

    def __str__(self):
        return self.name

    @staticmethod
    def from_db(connection_string, board_name):
        territory_select = """
                   EXEC [board].[board_select_territories] @board_name=?;
                   """
        continent_select = """
                           EXEC [board].[board_select_continents] @board_name=?;
                           """
        border_select = """
                        EXEC [board].[board_select_borders] @board_name=?;
                        """

        with pyodbc.connect(connection_string) as conn:
            cur = conn.cursor()
            params = [board_name]
            cur.execute(territory_select, params)
            territories_df = pd.DataFrame.from_records(
                cur.fetchall(),
                columns=[col[0] for col in cur.description]
            )

            cur.execute(continent_select, params)
            continents_df = pd.DataFrame.from_records(
                cur.fetchall(),
                columns=[col[0] for col in cur.description]
            )
            cur.execute(border_select, params)
            borders_df = pd.DataFrame.from_records(
                cur.fetchall(),
                columns=[col[0] for col in cur.description]
            )
            cur.close()

        G = nx.Graph()
        territories = {}
        continents = {}
        border_list = []
        for row in continents_df.itertuples():
            continent_name = row.continent_name
            supply_bonus = row.supply_bonus
            new_continent = Continent(
                name=continent_name,
                territories=[],
                supply_bonus=supply_bonus
            )
            continents[continent_name] = new_continent
            for territory in territories_df[
                    territories_df['continent_name'] == continent_name
                ].itertuples():
                name = territory.territory_name
                new_territory = Territory(
                    name=name
                )
                continents[continent_name].add_territory(new_territory)
                territories[name] = new_territory
                G.add_node(
                    new_territory,
                    label=name,
                    title=name,
                    group=continent_name
                )

        border_set = list(borders_df.itertuples(index=False, name=None))
        border_set = set(tuple(frozenset(sub)) for sub in set(border_set))

        for u, v in border_set:
            source_territory_name = u
            source_territory = territories[source_territory_name]
            destination_territory_name = v
            destination_territory = territories[destination_territory_name]
            G.add_edge(source_territory, destination_territory, penwidth=5)

        for node in G.nodes():
            source_territory = territories[node.name]
            for neighbor in G.neighbors(node):
                destination_territory = territories[neighbor.name]
                border = Border(
                    source_territory=source_territory,
                    destination_territory=destination_territory
                )
                source_territory.add_neighbor(destination_territory)
                border_list.append(border)
        return Board(
            territories=territories,
            borders=border_list,
            continents=continents,
            name=board_name
        )
    def owned_territories(self, player):
        owned_territories = []
        for territory_name in self.territories:
            territory = self.territories[territory_name]
            if territory.owner == player:
                owned_territories.append(territory)
        return owned_territories
    
    def unowned_territories(self):
        unowned_territories = []
        for territory_name in self.territories:
            territory = self.territories[territory_name]
            if territory.owner == None:
                unowned_territories.append(territory)
        return unowned_territories
    
    def owned_continents(self, player):
        owned_continents = []
        for continent_name in self.continents:
            continent = self.continents[continent_name]
            owner = continent.get_owner()
            if owner == player:
                owned_continents.append(continent)
        return owned_continents
    
    def legal_attacks(self, player):
        legal_attacks = []
        owned_terrs = self.owned_territories(player)
        for terr in owned_terrs:
            if terr.can_be_attack_source():
                legal_attacks.append(terr)
        return legal_attacks
    


