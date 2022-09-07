from risk.board.board import Board
from risk.game.game import Game
from risk.game.state import State
from risk.game.player import Player
from risk.agents.human_agent import HumanAgent
from risk.agents.random_agent import RandomAgent
from risk.auth.dbconnect import pyodbc_connstring
import os

def main(source, file_path=None):
    if source == 'yaml':
        board = Board.from_yaml(file_path, 'Original')
    if source == 'sql':
        board = Board.from_db(pyodbc_connstring(), 'Original')

    players = [
        Player('Rand_1', RandomAgent()),
        Player('Rand_2', RandomAgent()),
        Player('Rand_3', RandomAgent())
    ]
    game_state = State(
        board=board,
        players=players,
        deck=None
    )
    game = Game(game_state, verbose=False)
    game.state.random_start()
    game.state.update_nbsr()
    game.play_game()

if __name__ == "__main__":
    # source = None
    # response = None
    # while response not in {"sql", "yaml"}:
    #     response = input("Create board from SQL or YAML? ").lower()
    # 
    # if response == "sql":
    #     source = 'sql'
    #     file_path = None
    # if response == 'yaml':
    #     source = 'yaml'
    #     valid_path = 0
    #     while valid_path == 0:
    #         user_path = input('Please specify the target yaml file path: ')
    #         if user_path.endswith('.yaml') and os.path.exists(user_path):
    #             file_path = user_path
    #             valid_path = 1

    main('sql')
