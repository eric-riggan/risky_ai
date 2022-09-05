from risk.board.board import Board
from risk.game.game import Game
from risk.game.state import State
from risk.game.player import Player
from risk.agents.human_agent import HumanAgent
from risk.agents.random_agent import RandomAgent
from risk.auth.dbconnect import pyodbc_connstring

def main():
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
    game_board = Board.from_db(pyodbc_connstring(), 'Original')
    print(list(game_board.territories))

    main()
