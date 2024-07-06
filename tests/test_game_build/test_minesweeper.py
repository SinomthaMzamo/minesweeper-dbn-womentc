import unittest
from game_build.minesweeper import *


# TODO :  The game processes player moves according to the game rules
#  As a minesweeper game in progress
#  I want to process player moves according to the game rules
#  So that I can manage the state of the game and record the outcomes of player moves

# TODO :  The player reveals all the safe tiles on the board
#  As a minesweeper game in progress
#  I want to determine whether all safe tiles have been revealed
#  So that the game is ended in a win

# TODO :  The game detonates all remaining mines and ends the game when a mine tile is revealed
#  As a minesweeper game in progress
#  I want to detonate all the mines on the board
#  So that the game is ended in a loss

# TODO :  The game allows the player to toggle a limited number of flags
#  As a minesweeper game in progress
#  I want to regulate flag availability and usage
#  So that the player can't place more flags than there are mines
#  and can strategically mark/unmark suspected mine locations.

class TestGame(unittest.TestCase):
    def setUp(self):
        grid = Grid(9, 9)
        self.first_move_locale = (0, 0)
        self.test_game = Game(grid)

    def test_create_first_neighbourhood(self):
        # grid should only contain the first neighbourhood 
        pass

    def test_get_possible_mine_locales(self):
        # 
        pass

    def test_get_mine_locales(self):
        pass

    # TODO :  The game detonates all remaining mines and ends the game when a mine tile is revealed
    #  As a minesweeper game in progress
    #  I want to detonate all the mines on the board
    #  So that the game is ended in a loss
    def test_deploy_mines(self):
        pass

    def test_set_up_game_tiles(self):
        pass

    # TODO :  The player reveals all the safe tiles on the board
    #  As a minesweeper game in progress
    #  I want to determine whether all safe tiles have been revealed
    #  So that the game is ended in a win
    def test_check_win(self):
        pass

    def test_game_over(self):
        pass

    # TODO :  The game allows the player to toggle a limited number of flags
    #  As a minesweeper game in progress
    #  I want to regulate flag availability and usage
    #  So that the player can't place more flags than there are mines
    #  and can strategically mark/unmark suspected mine locations.
    def test_flags(self):
        pass



    # TODO :  The game processes player moves according to the game rules
    #  As a minesweeper game in progress
    #  I want to process player moves according to the game rules
    #  So that I can manage the state of the game and record the outcomes of player moves
    def test_run_game(self):
        pass


