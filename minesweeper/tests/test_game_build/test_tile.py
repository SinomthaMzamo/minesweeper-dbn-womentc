import unittest
from game_build.tile import *

class TestTile(unittest.TestCase):
    def setUp(self) -> None:
        self.basic_attr = { 
            "locale": (0,0),
            "size": 5,
            "is_revealed": False,
            "is_flagged": False
        }
        self.locale, self.size = [self.basic_attr.get(attr) for attr in ("locale", "size")]
        
    def test_basic_attributes_inherited(self):
        ''' test that tiles are initialized as expected 
            i.e. parent class attributes successfully inherited by child classes
        '''
        locale, size = self.locale, self.size   
        basic_attr = self.basic_attr

        basicTile = Tile(locale, size)
        safeTile = SafeTile(locale, size)
        mineTile = MineTile(locale, size)

        for tile in [basicTile, safeTile, mineTile]:
            for k,v in basic_attr.items():
                self.assertEqual(getattr(tile,k,None),v)

    # TEST PARTICULAR ATTRIBUTES MANJE
    def test_safe_tile_initially(self):
        ''' test SafeTile private attributes upon initialization 
        '''
        safeTile = SafeTile(self.locale, self.size)

        self.assertEqual([], safeTile.neighbours)
        self.assertIsNone(safeTile.totally_safe)

    def test_mine_tile_initially(self):
        ''' test MineTile private attributes upon initialization 
        '''
        mineTile = MineTile(self.locale, self.size)
        self.assertIsInstance(mineTile, MineTile)

    def test_toggle_flag(self):
        pass

    def test_reveal_totally_safe_tile(self):
        # tile.is_revealed should = True
        # neighbours too
        pass
    
    def test_reveal_somewhat_safe_tile(self):
        # tile.is_revealed should = True
        # neighbours unchanged
        pass

    def test_reveal_mine_tile(self):
        # tile.is_revealed should = True
        # all other mines too
        pass

    def test_count_mines_in_neighbourhood(self):
        pass

    def test_show_neighbourhood_info(self):
        # only show for revealed tiles
        pass