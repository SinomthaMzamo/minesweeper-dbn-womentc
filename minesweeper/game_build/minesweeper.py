import game_build.tile
from game_build.grid import Grid
from game_build.tile import MineTile, SafeTile, Tile
from random import choice, sample, shuffle

class Board:
    def __init__(self, mode):
        self.grid = None
        self.mode = mode
        self.tile_size = None
        self.mine_count = None
        self.all_mines = []
        self.safe_tiles = []
        self.apply_game_settings(mode)

    def apply_game_settings(self, mode):
        """       **** In development
        Set up the game modes and define difficulty levels and constructs grid accordingly.
        """
        # set tile size here

        difficulty_levels = {
            "pops": {"size": 10, "mine_count": 60},
            "test": {"size": 4, "mine_count":3},
            "easy": {"size": 9, "mine_count": 10},
            "medium": {"size": 16, "mine_count": 40},
            "hard": {"size": 24, "mine_count": 99}
        }

        mode_info = difficulty_levels[self.mode.lower()]
        self.mine_count = mode_info["mine_count"]
        rows = columns = mode_info.get("size", 9)
        self.grid = Grid(rows, columns)
        print(f'game settings: {mode.upper()} {rows}x{columns}')

    def set_up_game_tiles(self, first_move_locale):
        """
        Set up the game grid and tiles.

        Args:
        - first_move_locale (tuple): Coordinates (row, column) of the first move.
        """
        # randomly place mines outside of first move radius 
        self.deploy_mines(first_move_locale)
        self.all_mines = [tile for tile in self.grid.contents if not hasattr(tile[0],"totally_safe") and not isinstance(tile[0], tuple)]
        
        # fill up the rest of the grid with safe tiles
        for i, row in enumerate(self.grid.matrix):
            for j, tile in enumerate(row):
                self.make_tile((i,j))
        self.safe_tiles = [tile for tile in self.grid.contents if tile not in self.all_mines]

        # final stages of grid-tile setup
        for tile in self.safe_tiles:
            tile = tile[0]
            tile.totally_safe = not tile.count_neighbourhood_mines()

    def make_tile(self, locale, is_mine=False):
        """
        Create a specified tile using the relevant tile subclass and add it to the grid.

        Args:
            locale (tuple): Coordinates (row, column) for the new tile.
            is_mine (bool): Flag indicating whether the tile is a mine.

        Returns:
            Tile: The created tile object.
        """
        try:
            i, j = locale
        except TypeError:
            pass
        else:
            tile_phase = self.grid.matrix[i][j][0]
            # only make a tile at locales without tiles
            if isinstance(tile_phase, tuple):
                # make tile depending on required kind
                tile = MineTile(locale, self.tile_size) if is_mine else SafeTile(locale, self.tile_size)
                # populate grid with tile
                self.grid.replace_locale_with_tile_on_grid(tile)
                # set its neighbours if safe tile was created 
                if not is_mine:
                    tile.neighbours = self.grid.tile_adjacency_map[locale]
                return tile

    def create_first_neighbourhood(self, first_move_locale):
        """
        Create the first neighbourhood of tiles around the initial move locale.

        Args:
        - first_move_locale (tuple): Coordinates (row, column) of the first move.
        
        Returns:
        - first_tile (SafeTile): The tile at the first move locale.
        """
        grid = self.grid
        tile_adjacency_map = grid.get_tile_adjacency()

        first_tile = self.make_tile(first_move_locale)
        first_neighbourhood_locales = tile_adjacency_map[first_move_locale]
        [self.make_tile(loc[0]) for loc in first_neighbourhood_locales]

        return first_tile

    def get_mine_locales(self, first_move_locale):
        """
        Get random mine locales based on the game difficulty.

        Args:
        - first_move_locale (tuple): Coordinates (row, column) of the first move.

        Returns:
        - list of tuple[int, int]: A list of mine locales.
        """
    
        mine_count = self.mine_count
        # ensure first move's neighbourhood consists only of safe tiles
        first_move_tile = self.create_first_neighbourhood(first_move_locale)
        
        # generate locales for mine tiles, these locales need to lie outside the first move's neighbourhood/radius
        mine_territory_locales = self.get_possible_mine_locales(first_move_tile)
        shuffle(mine_territory_locales)
        return sample(mine_territory_locales, mine_count)

    def deploy_mines(self, first_move_locale):
            """
            Deploy mines on the grid based on the first move locale.

            Args:
            - first_move_locale (tuple): Coordinates (row, column) of the first move.
            """
            game_mine_locales = self.get_mine_locales(first_move_locale)

            for mine_locale in game_mine_locales:
                self.make_tile(mine_locale, is_mine=True)

    def set_up_game_board(self, first_move_locale):
        """Set up the game board, including placing mines and safe tiles.

        Args:
        - first_move_locale (tuple): Coordinates (row, column) of the first move.
        """
        self.set_up_game_tiles(first_move_locale)
        self.game_reveal(first_move_locale)

    def game_reveal(self, locale):
        """
        Reveal the chosen tile at the specified locale.

        Args:
        - locale (tuple): Coordinates (row, column) of the tile.
        """
        i,j = locale
        # reveal chosen tile
        self.grid.matrix[i][j][0].reveal()

    def get_possible_mine_locales(self, first_move_tile):
        """
        Process the player's first move by determining the possible mine territory i.e. the region outside of the first move's neighbourhood tiles.

        Args:
        - first_move_tile (SafeTile): The selected tile at the first move locale.

        Returns:
        - list of tuple[int, int]: A list of possible locales where mines might be placed.
        """
        grid = self.grid
        matrix = grid.matrix
        x,y = first_move_tile.locale

        first_neighbourhood_tiles = [matrix[x][y]] + first_move_tile.neighbours
        first_neighbourhood_locales = [tile[0].locale for tile in first_neighbourhood_tiles]

        possible_mine_territory_locales = [(i, j) for i, row in enumerate(matrix) for j, _ in enumerate(row) if (i, j) not in first_neighbourhood_locales]
        return possible_mine_territory_locales

    def get_rows(self):
        return self.grid.rows

    def get_columns(self):
        return self.grid.columns

    def get_tile_from_locale(self, locale: tuple) -> Tile:
        i, j = locale
        return self.grid.matrix[i][j][0]

    def get_tile_size(self, width: int):
        return width // self.get_columns()

class Game:
    """ Runs the logic and flow of game:
        - Sets up game components i.e. tiles, grid
        - Handles first move control and distribution of mines
        - Handles flag use and restriction
        - Handles game major events:
            * revealing a mine tile
            * revealing all safe tiles

    """
 
    def __init__(self, board):
        """
        Initialize the Game object.

        Attributes:
        - board (Board): The game board.
        - in_play (bool): Flag indicating whether the game is in progress.
        - tile_size (None): Placeholder for the size of each tile (to be set later).
        - flags_placed (int): Number of flags placed.
        """
     
        self.in_play = False
        self.board = board
        # self.tile_size = None           # depends on grid dimensions and is irrelevant until GUI stage
        self.flags_placed = 0

    def run_game(self, this_move, flag=False):
        """
        Run the main game loop.
        """
        # start the game
        self.in_play = True
        
        if self.in_play:
            if flag:
                self.handle_flag_limit_and_usage(this_move)
                print("toggling flag...")
                return
            
            self.board.game_reveal(this_move)

            # exits game loop if reveal resulted in a win
            self.check_win()
        
            if not all(not tile[0].is_revealed for tile in self.board.all_mines) :
                self.game_over()

    def check_win(self):
        """
        Check if the player has won the game.
        """
        safe_tiles = self.board.safe_tiles
        # it's a win when all safe_tiles are uncovered without uncovering a mine tile 
        win = all(tile[0].is_revealed for tile in safe_tiles) and all(not tile[0].is_revealed for tile in self.board.all_mines)
        if win:
            self.in_play = False
            self.game_over(win=True)

    def detonate_all_mines(self):
        """
        Detonate all mine tiles and end the game.
        """
        all_mines = self.board.all_mines
        print("detonating", all_mines, "mines.")
        # uncover all mines
        for tile in all_mines:
            tile[0].reveal()


        # TO_DO: take note of how many were correctly flagged and show this

    def game_over(self, win=False):
        """         **** In development
        Handle the end of the game.

        Args:
        - win (bool): Flag indicating whether the player won.
        """
        if win:
            # do win sequence, GUI tings
            pass
        else:
            print("initiatiing loss sequence...")
            self.detonate_all_mines()   
            print("you lose.")     
            self.in_play = False

    def handle_flag_limit_and_usage(self, tile_locale):
        """
        Handle flag limit and usage logic.

        Args:
        - tile_locale (tuple): Coordinates (row, column) of the selected tile.
        """
        i,j = tile_locale
        tile = self.get_game_board().get_tile_from_locale(tile_locale)
        print(self.board.mine_count - self.flags_placed)
        if self.flags_placed <= self.board.mine_count:
            # don't place a flag if flag limit reached
            if not tile.is_flagged and self.flags_placed >= self.board.mine_count:
                    return
            tile.toggle_flag()

            # reduce or increment available flags depending on whether a flag was placed or removed
            if tile.is_flagged:
                self.flags_placed += 1
                print("flag placed at: ", tile_locale)
            else:
                self.flags_placed -= 1
                print("flag removed at: ", tile_locale)

    def get_game_board(self) -> Board:
        return self.board

    def get_number_of_flags_placed(self):
        return self.flags_placed

    def get_mine_count(self):
        return self.board.mine_count
