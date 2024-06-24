from game_build.minesweeper import Game, Board
from random import choice


def play_minesweeper():
    # get game mode
    game_modes = ["easy", "medium", "hard"]
    mode = choice(game_modes)

    # create Board instance
    board1 = Board(mode)

    # create Game instance 
    minesweeper = Game(board1)

    # get first move
    first_move_locale = choice(board1.grid.contents)[0]

    # set up the game board (distribution of mines)
    minesweeper.board.set_up_game_board(first_move_locale)

    # start game loop
    minesweeper.run_game(first_move_locale)


if __name__ == "__main__":
    play_minesweeper()
    

    

    