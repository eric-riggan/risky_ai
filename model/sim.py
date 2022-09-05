import pandas as pd
import numpy as np
from uuid6 import uuid6
import sys
import pyodbc
from alive_progress import alive_bar
import yaml

def pyodbc_connstring():
    with open('risk/auth/db_auth.yaml', 'r', encoding='utf8') as stream:
        config = yaml.safe_load(stream)
        connstring = f"DRIVER={{{config['driver']}}};SERVER={config['server']};DATABASE={config['database']};UID={config['username']};PWD={config['password']};Encrypt=YES;TrustServerCertificate=YES"
        return connstring

generator = np.random.PCG64()
randomizer = np.random.Generator(generator)

# Functions
def sort_2(l):
    '''
    Sorts a list of size n = 2
    '''
    if l[0] < l[1]:
        return [l[i] for i in [1, 0]]
    else:
        return l

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

# define dice_sort - sorts lists of n = 2 or 3
dice_sort = [None, lambda l: l, sort_2, sort_3]

# define attack function

def attack(attackers, defenders, losses=False):
    '''
    runs Risk attack for one attack round.
    Returns the resultant army sizes. If losses=True,
    also returns the number of losses each side sustained.
    '''
    attacker_losses = 0
    defender_losses = 0
    # get number of dice to roll for each side
    if attackers > 0 and defenders > 0:
        if attackers >= 3:
            atk_dice = 3
        if attackers == 2:
            atk_dice = 2
        if attackers == 1:
            atk_dice = 1
        if defenders >= 2:
            def_dice = 2
        if defenders == 1:
            def_dice = 1
        # get rolled dice for each side
        rolls = list(
            zip(
                dice_sort[atk_dice](
                    randomizer.integers(
                        low=1,
                        high=6,
                        endpoint=True,
                        size=atk_dice
                    ).tolist()
                ),
                dice_sort[def_dice](
                    randomizer.integers(
                        low=1,
                        high=6,
                        endpoint=True,
                        size=def_dice
                    ).tolist()
                )
            )
        )
        # Get number of losses sustained by each side
        for roll in rolls:
            if roll[0] > roll[1]:
                defenders -= 1
                if losses == True:
                    defender_losses += 1
            else:
                attackers -= 1
                if losses == True:
                    attacker_losses += 1
        if losses == True:                    
            return [attackers, defenders, attacker_losses, defender_losses]
        else:
            return [attackers, defenders]
    else:
        sys.exit(1)

# engine.execute(
#     statement='TRUNCATE TABLE `risk`.`sim_rounds`;'
# )
# engine.execute(
#     statement='TRUNCATE TABLE `risk`.`sim_games`;'
# )

def conquer(atk_str, def_str, matches_played=1):
    matches = []
    match_rounds = []
    for i in range(1, matches_played + 1, 1):
        # match_id += 1
        # match_id = uuid6().bytes
        match_id = str(uuid6())
        game_id = match_id
        game = {
            "id": game_id,
            "atk_strength": atk_str,
            "def_strength": def_str,
        }
        game_rounds = 0
        atk_losses_cumul = 0
        def_losses_cumul = 0
        atk_armies = game['atk_strength']
        def_armies = game['def_strength']
        while atk_armies > 0 and def_armies > 0:
            game_rounds += 1
            attack_round = {
                # "id": uuid6().bytes,
                "id": str(uuid6()),
                "game_id": match_id,
                "atk_strength": atk_armies,
                "def_strength": def_armies
            }
            atk_armies, def_armies, atk_losses, def_losses = attack(
                attackers=atk_armies,
                defenders=def_armies,
                losses=True
            )
            attack_round['atk_losses'] = atk_losses
            attack_round['def_losses'] = def_losses
            if atk_losses > def_losses:
                attack_round['outcome'] = 0
            elif def_losses > atk_losses:
                attack_round['outcome'] = 1
            else:
                attack_round['outcome'] = None
            match_rounds.append(attack_round)
            atk_losses_cumul = atk_losses_cumul + atk_losses
            def_losses_cumul = def_losses_cumul + def_losses
            if atk_armies == 0 or def_armies == 0:
                game['rounds'] = game_rounds
                game['atk_losses'] = atk_losses_cumul
                game['def_losses'] = def_losses_cumul
                if def_armies == 0:
                    game['outcome'] = 1
                else:
                    game['outcome'] = 0
                matches.append(game)
    matches_df = pd.DataFrame(
        data=matches
    )
    match_rounds_df = pd.DataFrame(
        data=match_rounds
    )
    return matches_df, match_rounds_df

def truncate_db(connstring):
    conn = pyodbc.connect(connstring)
    cur = conn.cursor()
    cur.execute("""DELETE FROM [sim].[sim_games];""")
    cur.commit()
    cur.close()
    conn.close()

def conquer_db(atk_str, def_str, connstring, matches_played=1, save_rounds=False):
    # connection_url = URL.create(
    #     'mssql+pyodbc',
    #     query={
    #         'odbc_connect': connstring
    #     }
    # )
    # connengine = sa.create_engine(connection_url)
    ROUND_INSERT = """
                  INSERT INTO [risk].[sim].[sim_rounds] (
                      [id],
                      [game_id],
                      [atk_strength],
                      [def_strength],
                      [atk_losses],
                      [def_losses],
                      [outcome]
                  ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?
                  );
                  """
    GAME_INSERT = """
                  INSERT INTO [risk].[sim].[sim_games] (
                      [id],
                      [atk_strength],
                      [def_strength],
                      [atk_losses],
                      [def_losses],
                      [rounds],
                      [outcome]
                  ) VALUES (
                      ?, ?, ?, ?, ?, ?, ?
                  );
                  """
    GAME_UPDATE = """
                  UPDATE [risk].[sim].[sim_games]
                     SET [atk_losses] = ?,
                         [def_losses] = ?,
                         [rounds] = ?,
                         [outcome] = ?
                   WHERE [id] = ?;
                  """
    conn = pyodbc.connect(connstring)
    cur = conn.cursor()
    with alive_bar(matches_played) as progress_bar:
        for i in range(1, matches_played + 1, 1):
            # match_id += 1
            # match_id = uuid6().bytes
            match_id = str(uuid6())
            game = {
                "id": match_id,
                "atk_strength": atk_str,
                "def_strength": def_str,
            }
            cur.execute(
                GAME_INSERT,
                [
                    game['id'],
                    game['atk_strength'],
                    game['def_strength'],
                    0, 0, 0, 0
                ]
            )
            game_rounds = 0
            atk_losses_cumul = 0
            def_losses_cumul = 0
            atk_armies = game['atk_strength']
            def_armies = game['def_strength']
            while atk_armies > 0 and def_armies > 0:
                # match_rounds = []
                game_rounds += 1
                attack_round = {
                    # "id": uuid6().bytes,
                    "id": str(uuid6()),
                    "game_id": match_id,
                    "atk_strength": atk_armies,
                    "def_strength": def_armies
                }
                atk_armies, def_armies, atk_losses, def_losses = attack(
                    attackers=atk_armies,
                    defenders=def_armies,
                    losses=True
                )
                attack_round['atk_losses'] = atk_losses
                attack_round['def_losses'] = def_losses
                if atk_losses > def_losses:
                    attack_round['outcome'] = 0
                elif def_losses > atk_losses:
                    attack_round['outcome'] = 1
                else:
                    attack_round['outcome'] = None
                # match_rounds.append(attack_round)
                if save_rounds is True:
                    cur.execute(
                        ROUND_INSERT,
                        [
                            attack_round['id'],
                            attack_round['game_id'],
                            attack_round['atk_strength'],
                            attack_round['def_strength'],
                            attack_round['atk_losses'],
                            attack_round['def_losses'],
                            attack_round['outcome']
                        ]
                    )
                atk_losses_cumul = atk_losses_cumul + atk_losses
                def_losses_cumul = def_losses_cumul + def_losses
                if atk_armies == 0 or def_armies == 0:
                    game['rounds'] = game_rounds
                    game['atk_losses'] = atk_losses_cumul
                    game['def_losses'] = def_losses_cumul
                    if def_armies == 0:
                        game['outcome'] = 1
                    else:
                        game['outcome'] = 0
                    cur.execute(
                        GAME_UPDATE,
                        [
                            game['atk_losses'],
                            game['def_losses'],
                            game['rounds'],
                            game['outcome'],
                            game['id']
                        ]
                    )
                    cur.commit()
                    progress_bar()
        cur.close()
        conn.close()

# truncate_db(connection_string)
GAMES_SIM = 10000

# for i in range(1,31,1):
#     for k in range(1,31,1):
#         print(f'ATTACKERS: {i}. DEFENDERS: {k}.')
#         conquer_db(
#             atk_str=i,
#             def_str=k,
#             connstring=connection_string,
#             matches_played=GAMES_SIM,
#             save_rounds=False
#         )
