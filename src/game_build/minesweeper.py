import enum
import json

from src.game_build.grid import Grid
from src.game_build.tile import MineTile, SafeTile, Tile
from random import choice, sample, shuffle


class ModeFactory:
    # todo: mode factory generates a default make
    #   As a mode factory
    #   I want to generate default make objects based on predefined values
    #   So that there can be a level of automation in game setup
    def __init__(self):
        self.preset_modes = {
            "sandy-baby": {"size": 50, "mine_count": 230},
            "pops": {"size": 10, "mine_count": 60},
            "test": {"size": 5, "mine_count": 2},
            "easy": {"size": 9, "mine_count": 10},
            "medium": {"size": 16, "mine_count": 40},
            "hard": {"size": 24, "mine_count": 99}
        }

    def generate_preset_mode(self, mode_name: str):
        size, mine_count = self.preset_modes.get(mode_name).get("size"), self.preset_modes.get(mode_name).get("mine_count")
        mine_percentage = round(mine_count/(size**2)*100)
        return Mode(size, mine_percentage)

    def generate_custom_mode(self, size, mine_percentage):
        return Mode(size, mine_percentage)





class Mode:
    def __init__(self, size, mine_percentage=50):
        self.size = size
        self.mine_count = self.get_mine_count_from_percentage_of_mines(mine_percentage)

    def get_mine_count_from_percentage_of_mines(self, mine_percentage):
        return round(self.size ** 2 * (mine_percentage / 100))

    def get_mine_count(self):
        return self.mine_count

    def get_size(self):
        return self.size


class Board:
    def __init__(self, mode: Mode):
        self.grid = None
        self.mode = mode
        self.tile_size = None
        self.mine_count = None
        self.all_mines = []
        self.safe_tiles = []
        self.apply(mode)

    # TODO : the board story:
    #  The board generates a grid and game configuration from user selected mode
    #  As a square board of minesweeper tiles
    #  I want to configure the minesweeper game based on player stipulations
    #  So that i can generate the desired grid
    def apply_game_settings(self, mode):
        """       **** In development
        Set up the game modes and define difficulty levels and constructs grid accordingly.
        """
        # set tile size here

        difficulty_levels = {
            "sandy-baby": {"size": 50, "mine_count": 230},
            "pops": {"size": 10, "mine_count": 60},
            "test": {"size": 5, "mine_count": 2},
            "easy": {"size": 9, "mine_count": 10},
            "medium": {"size": 16, "mine_count": 40},
            "hard": {"size": 24, "mine_count": 99}
        }

        mode_info = difficulty_levels[mode.lower()]
        self.mine_count = mode_info["mine_count"]
        rows = columns = mode_info.get("size", 9)
        self.grid = Grid(rows, columns)
        print(f'game settings: {mode.upper()} {rows}x{columns}', "mines:", self.mine_count)

    def apply(self, mode: Mode):
        self.mine_count = mode.get_mine_count()
        rows = columns = mode.get_size()
        self.grid = Grid(rows, columns)

    def customise_board(self, size, mine_percentage):
        return Mode(size, mine_percentage)

    # TODO :  The board populates a grid with SafeTiles and MineTiles based on game configuration upon first move
    #  As a square board of minesweeper tiles
    #  I want to configure the minesweeper game based on player's first move
    #  So that I can randomise the placement of bombs, while ensuring the first neighbourhood is safe
    def set_up_game_tiles(self, first_move_locale):
        """
        Set up the game grid and tiles.

        Args:
        - first_move_locale (tuple): Coordinates (row, column) of the first move.
        """
        # randomly place mines outside first move radius
        self.deploy_mines(first_move_locale)

        # fill up the rest of the grid with safe tiles
        for i in range(self.grid.rows):
            for j in range(self.grid.columns):
                self.make_tile((i, j))

        for tile in self.grid.contents.flat:
            if isinstance(tile, SafeTile):
                self.safe_tiles.append(tile)
            elif isinstance(tile, MineTile):
                self.all_mines.append(tile)

        self.grid.update_adjacency()
        # final stages of grid-tile setup
        for tile in self.safe_tiles:
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
            return locale
        else:
            tile_phase = self.grid.contents[i, j]
            if is_mine:
                print("i should be a tuple ->", tile_phase)
            # only make a tile at locales without tiles
            if isinstance(tile_phase, tuple):
                # make tile depending on required kind
                tile = MineTile(locale, self.tile_size) if is_mine else SafeTile(locale, self.tile_size)
                # populate grid with tile
                self.grid.contents[i, j] = tile

                return tile

    def create_first_neighbourhood(self, first_move_locale) -> SafeTile:
        """
        Create the first neighbourhood of tiles around the initial move locale.

        Args:
        - first_move_locale (tuple): Coordinates (row, column) of the first move.

        Returns:
        - first_tile (SafeTile): The tile at the first move locale.
        """

        first_tile = self.make_tile(first_move_locale)
        first_neighbourhood_locales = self.grid.tile_adjacency_map[first_move_locale]
        first_neighbourhood_tiles = [self.make_tile(loc) for loc in first_neighbourhood_locales]
        first_tile.neighbours = first_neighbourhood_tiles

        return first_tile

    def get_mine_locales(self, first_move_locale):
        """
        Get random mine locales based on the game difficulty.

        Args:
        - first_move_locale (tuple): Coordinates (row, column) of the first move.

        Returns:
        - list of tuple[int, int]: A list of mine locales.
        """

        # ensure first move's neighbourhood consists only of safe tiles
        first_move_tile = self.create_first_neighbourhood(first_move_locale)

        # generate locales for mine tiles, these locales need to lie outside the first move's neighbourhood/radius
        mine_territory_locales = self.get_possible_mine_locales(first_move_tile)
        shuffle(mine_territory_locales)
        return sample(mine_territory_locales, self.mine_count)

    def deploy_mines(self, first_move_locale):
        """
        Deploy mines on the grid based on the first move locale.

        Args:
        - first_move_locale (tuple): Coordinates (row, column) of the first move.
        """
        mine_locales = self.get_mine_locales(first_move_locale)
        print(f"mine locales: {mine_locales}\npress enter to proceed")
        for mine_locale in mine_locales:
            mine = self.make_tile(mine_locale, is_mine=True)
            print(mine, "at", mine_locale)

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
        i, j = locale
        # reveal chosen tile
        self.grid.matrix[i, j].reveal()
        return self.grid.matrix[i, j]

    def get_possible_mine_locales(self, first_move_tile: SafeTile):
        """
        Process the player's first move by determining the possible mine territory i.e. the region outside of the first move's neighbourhood tiles.

        Args:
        - first_move_tile (SafeTile): The selected tile at the first move locale.

        Returns:
        - list of tuple[int, int]: A list of possible locales where mines might be placed.
        """

        first_neighbourhood_tiles = [first_move_tile] + first_move_tile.neighbours
        first_neighbourhood_locales = [tile.locale for tile in first_neighbourhood_tiles]

        possible_mine_territory_locales = [(row, col) for row in range(self.grid.rows)
                                           for col in range(self.grid.columns)
                                           if (row, col) not in first_neighbourhood_locales]

        return possible_mine_territory_locales

    def get_rows(self):
        return self.grid.rows

    def get_columns(self):
        return self.grid.columns

    def get_tile_from_locale(self, locale: tuple) -> Tile:
        i, j = locale
        return self.grid.matrix[i, j]

    def get_tile_size(self, width: int):
        return width // self.get_columns()


class Outcome(enum.Enum):
    Win = "win"
    Play = "play"
    Lose = "lose"


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
        self.refresh()
        self.in_play = False
        self.board = board
        # self.tile_size = None           # depends on grid dimensions and is irrelevant until GUI stage
        self.flags_placed = 0

    def refresh(self):
        path = "this_round.json"

        with open(path, "w") as file:
            json.dump("", file)

    # TODO :  The game processes player moves according to the game rules
    #  As a minesweeper game in progress
    #  I want to process player moves according to the game rules
    #  So that I can manage the state of the game and record the outcomes of player moves

    def handle_selection(self, this_move, flag=False):
        """
        Run the main game loop.
        """
        outcome = None
        flagged_tile = revealed_tile = None
        print(self.is_in_play(), "that the game is still running")
        if self.in_play:
            if flag:
                flagged_tile = self.handle_flag_limit_and_usage(this_move)
                print("toggling flag...")
                outcome = Outcome.Play.value
            else:
                revealed_tile = self.board.game_reveal(this_move)  # capture the revealed tile object
                if all(tile.is_revealed for tile in self.board.safe_tiles) and all(
                        not tile.is_revealed for tile in self.board.all_mines):
                    outcome = Outcome.Win.value
                    self.game_over(win=True)
                elif any(tile.is_revealed for tile in self.board.all_mines):
                    outcome = Outcome.Lose.value
                    self.game_over(win=False)
                else:
                    outcome = Outcome.Play.value
        print(self.is_in_play(), "that the game is still running")
        """
        {
            "event": "win/lose/none",
            "tile": (0,0),
            ""
        }
        """
        json_outcome = {"outcome": outcome,
                        "tile": (flagged_tile.locale if not revealed_tile else revealed_tile.locale)}
        path = "this_round.json"

        with open(path, "w") as file:
            json.dump(json_outcome, file)

        print("saved")

        return flagged_tile if not revealed_tile else revealed_tile

    # TODO :  The player reveals all the safe tiles on the board
    #  As a minesweeper game in progress
    #  I want to determine whether all safe tiles have been revealed
    #  So that the game is ended in a win
    def check_win(self):
        """
        Check if the player has won the game.
        """
        safe_tiles = self.board.safe_tiles
        # it's a win when all safe_tiles are uncovered without uncovering a mine tile
        win = all(tile[0].is_revealed for tile in safe_tiles) and all(
            not tile[0].is_revealed for tile in self.board.all_mines)
        if win:
            self.in_play = False
            self.game_over(win=True)

    # TODO :  The game detonates all remaining mines and ends the game when a mine tile is revealed
    #  As a minesweeper game in progress
    #  I want to detonate all the mines on the board
    #  So that the game is ended in a loss
    def detonate_all_mines(self):
        """
        Detonate all mine tiles and end the game.
        """
        all_mines = self.board.all_mines
        print("detonating", all_mines, "mines.")
        # uncover all mines
        for tile in all_mines:
            tile.reveal()

        # TO_DO: take note of how many were correctly flagged and show this
        # should i reset in_play here?

    def game_over(self, win=False):
        """         **** In development
        Handle the end of the game.

        Args:
        - win (bool): Flag indicating whether the player won.
        """
        if win:
            # do win sequence, GUI tings
            print("you win!")
            pass
        else:
            print("initiatiing loss sequence...")
            self.detonate_all_mines()
            print("you lose.")
        self.in_play = False

    # TODO :  The game allows the player to toggle a limited number of flags
    #  As a minesweeper game in progress
    #  I want to regulate flag availability and usage
    #  So that the player can't place more flags than there are mines
    #  and can strategically mark/unmark suspected mine locations.
    def handle_flag_limit_and_usage(self, tile_locale):
        """
        Handle flag limit and usage logic.

        Args:
        - tile_locale (tuple): Coordinates (row, column) of the selected tile.
        """
        tile = self.get_game_board().get_tile_from_locale(tile_locale)

        # if flags placed < limit proceed as normal
        if self.flags_placed < self.board.mine_count:
            tile.toggle_flag()
            # reduce or increment available flags depending on whether a flag was placed or removed
            self.flags_placed += 1 if tile.is_flagged else -1
        else:
            if tile.is_flagged:
                tile.toggle_flag()
                self.flags_placed -= 1
        return tile

    def get_game_board(self) -> Board:
        return self.board

    def get_number_of_flags_placed(self):
        return self.flags_placed

    def get_mine_count(self):
        return self.board.mine_count

    def is_in_play(self):
        return self.in_play

    def setup(self, first_locale: tuple):
        self.get_game_board().set_up_game_board(first_locale)
        # start the game
        self.in_play = True
        self.handle_selection(first_locale)
