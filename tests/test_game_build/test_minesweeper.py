import unittest
from game_build.minesweeper import *

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

    def test_deploy_mines(self):
        pass

    def test_set_up_game_tiles(self):
        pass

    def test_check_win(self):
        pass

    def test_game_over(self):
        pass
    
    def test_run_game(self):
        pass