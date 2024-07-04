class Tile:
    """ Parent "Tile" class with child classes SafeTile and MineTile.
        Shared attributes and methods will be defined here 
        to introduce the idea of 'Inheritance' in OOP.
    """
    def __init__(self, locale, size):
        """
        Initialize a Tile object.

        Args:
        - locale (tuple): locale (row, column) of the tile on grid.
        - size (int): Size of the tile.
        """
        self.locale = locale
        self.size = size
        self.is_revealed = False
        self.is_flagged = False

    def reveal(self):        
        """
        Reveal the tile and handle the consequences.

        """
        if self.is_revealed:
            return
        # reveal the tile
        self.is_revealed = True
        self.process_reveal()


    def process_reveal(self):
        print(f'revealed generic tile at {self.locale}')


    def toggle_flag(self):
        """
        place and remove the flag on the tile if it's covered.
        """
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged

class SafeTile(Tile):
    """
    A subclass of Tile representing a safe tile in the Minesweeper game.

    Attributes:
    (Inherited)
    - locale (tuple): locale (row, column) of the tile on grid.
    - size (int): Size of the tile.
    - is_revealed (bool): Indicates whether the tile is revealed.
    - is_flagged (bool): Indicates whether the tile is flagged.
    (Local to child)
    - neighbours (list): List of neighbouring tiles.
    - totally_safe (bool): Indicates whether the tile is entirely safe.

    """

    def __init__(self, locale, size):
        """
        Initialize a SafeTile object.

        Args:
        - locale (tuple): locale (row, column) of the tile.
        - size (int): Size of the tile.
        """
        super().__init__(locale, size)
        self.neighbours = []
        self.totally_safe = None


    def process_reveal(self):
        # print(f'revealed SafeTile at {self.locale}')

        # show all tiles in neighbourhood if a totally safe tile was revealed 
        if getattr(self, "totally_safe", None):
            print(f'doing bubble for neighbours of {self.locale}...')
            for tile in self.neighbours:
                tile.reveal()

        # show number of unsafe neighbours if a somewhat safe tile was revealed 
        else:
            self.show_neigbourhood_info()
        

    def count_neighbourhood_mines(self):
        """
        Count the number of mines in the tile's neighborhood.

        Returns:
        - int: The number of mines in the tile's neighborhood.
        """
        unsafe_neighbours = [n for n in self.neighbours if not hasattr(n, "totally_safe") and not isinstance(n, tuple)]
        face_num = len(unsafe_neighbours)
        return face_num
    
    def show_neigbourhood_info(self):
        """
        Display information about the neighborhood if the tile is revealed.
        """
        if self.is_revealed:
            print(self.count_neighbourhood_mines())

class MineTile(Tile):
    """
    A subclass of Tile representing a mine tile in the Minesweeper game.

    Attributes:
    (Inherited)
    - locale (tuple): locale (row, column) of the tile on grid.
    - size (int): Size of the tile.
    - is_revealed (bool): Indicates whether the tile is revealed.
    - is_flagged (bool): Indicates whether the tile is flagged.
    
    """
    
    def __init__(self, locale, size):
        """
        Initialize a MineTile object.

        Args:
        - locale (tuple): locale (row, column) of the tile.
        - size (int): Size of the tile.
        """
        super().__init__(locale, size)

    def process_reveal(self):
        print(f'revealed MineTile at {self.locale}')
