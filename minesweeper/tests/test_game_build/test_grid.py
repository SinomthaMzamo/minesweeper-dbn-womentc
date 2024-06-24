import unittest
from game_build.grid import *
class TestGrid(unittest.TestCase):
    def setUp(self):
        self.rows = self.columns = 3
        self.grid = Grid(self.rows, self.columns)

        self.expected_basic = {"rows": self.rows, "columns": self.columns, "tile_size": None,}
        self.expected_contents = [
            [(0, 0)],[(0, 1)],[(0, 2)],
            [(1, 0)],[(1, 1)],[(1, 2)],
            [(2, 0)],[(2, 1)],[(2, 2)]
            ]
        
        self.expected_matrix = [
            [[(0, 0)], [(0, 1)], [(0, 2)]],
            [[(1, 0)], [(1, 1)], [(1, 2)]],
            [[(2, 0)], [(2, 1)], [(2, 2)]]
            ]
        
        self.expected_adjacency = {
            '(0, 0)': [[(0, 1)], [(1, 0)], [(1, 1)]],
            '(0, 1)': [[(0, 0)], [(0, 2)], [(1, 0)], [(1, 1)], [(1, 2)]],
            '(0, 2)': [[(0, 1)], [(1, 1)], [(1, 2)]],
            '(1, 0)': [[(0, 0)], [(0, 1)], [(1, 1)], [(2, 0)], [(2, 1)]],
            '(1, 1)': [[(0, 0)], [(0, 1)], [(0, 2)], [(1, 0)], [(1, 2)], [(2, 0)], [(2, 1)], [(2, 2)]],
            '(1, 2)': [[(0, 1)], [(0, 2)], [(1, 1)], [(2, 1)], [(2, 2)]],
            '(2, 0)': [[(1, 0)], [(1, 1)], [(2, 1)]],
            '(2, 1)': [[(1, 0)], [(1, 1)], [(1, 2)], [(2, 0)], [(2, 2)]],
            '(2, 2)': [[(1, 1)], [(1, 2)], [(2, 1)]]
            }
        
        self.expected_iterables = {"contents": self.expected_contents, "matrix":self.expected_matrix, "tile_adjacency_map":self.expected_adjacency}
        
    def test_grid_initial_state_basics(self):

        # Test basic attributes
        for k, v in self.expected_basic.items():
            self.assertEqual(getattr(self.grid, k, False), v, f"grid '{k}' attribute value should be '{v}' upon initialisation.")
        
        # Test iterable attributes
        self.assertTrue(all(hasattr(self.grid, attribute) for attribute in self.expected_iterables))  #redundant
        self.assertTrue(all(isinstance(getattr(self.grid,attribute, None),(list, dict)) for attribute in self.expected_iterables))
    
    
    def test_grid_initial_state_iterables_contents(self):
        # ensure that it's a list
        # has as many items in it as rows*colums
        # each item is a list containing a tuple
        # check if it's the right tuples
        pass


    def test_grid_initial_state_iterables_matrix(self):
        # ensure it is as a list
        # ensure it has as many items as there are rows
        # ensure each item is a list
        # each item must have as many contents as there are columns
        # ensure the contents are lists containing a tuple
        # check if it's the right tuples
        pass


    def test_grid_initial_state_iterables_adjacency(self):
        # ensure it is a dict
        # ensure it has as many items as rows*colums (it is a map of every tile's neighbourhood) 
            # or should it exclude bombs?
        # ensure the keys are strings of a tuple with tile location and the values are lists
            # the value list must contain items which are lists containing a tuple with tile locations
            # there must be as many items as the number of tiles touching that tile ON THE GRID
        pass

    def test_generate_full_neighbourhood_locales(self):
        pass

    def test_replace_locale_with_tile_on_grid(self):
        pass

    def test_make_tile(self):
        pass