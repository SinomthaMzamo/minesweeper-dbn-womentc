import numpy as np


# TODO : The get_matrix function currently uses a list comprehension to convert the
#  contents list to a matrix. This might become inefficient for larger grids.
# Explore alternative libraries like numpy for efficient multi-dimensional array handling.

class Grid:
    def __init__(self, rows, columns):
        """
        Initialize a grid with the specified number of rows and columns.

        Args:
        - rows (int): Number of rows in the grid.
        - columns (int): Number of columns in the grid.

        Attributes:
        - rows (int): Number of rows in the grid.
        - columns (int): Number of columns in the grid.
        - tile_size (None): Placeholder for the size of each tile (to be set later).
        - contents (list[list]): 2D list containing single Tile objects.
        - matrix (list of list[list]): 3D grid/matrix containing rows of Tile objects.
        - tile_adjacency_map (dict[str:list[list]]): Map of tile locales to their neighboring tiles.
        """
        self.rows, self.columns = rows, columns
        self.tile_size = None
        self.contents = np.empty((rows, columns), dtype=object)
        self.locale_to_index = {}
        self.matrix = self.get_matrix()
        self.tile_adjacency_map = self.get_tile_adjacency()
        self.set_tile_locales()
        print()

    def get_matrix(self):
        """
        Converts the list of grid items into a matrix format.

        Returns:
            list of list[list]: Matrix representation of the tiles in the grid.
            eg. a 3x3 matrix: [
                                [[],[],[]],
                                [[],[],[]],
                                [[],[],[]]
        ]
        """
        return self.contents

    def get_tile_adjacency(self):
        """
        Generate a map of tile locales to their neighboring tiles.

        Returns:
            dict: A dictionary mapping tile locales to lists of neighboring tiles.

            eg. an excerpt showing the neighbourhoods of the first row (3x3):
                {
                        "(0,0)": [[],[],[]],
                        "(0,1)": [[],[],[],[],[]],
                        "(0,2)": [[],[],[]],
                }
        """

        tile_adjacency = {}
        for x, row in enumerate(self.matrix):
            for y, _ in enumerate(row):
                possible_neighbours = self.generate_full_neighbourhood_locales((x, y))
                neighbours_on_grid = [(i, j) for i, j in possible_neighbours if
                                      i in range(self.rows) and j in range(self.columns)]
                tile_adjacency[(x, y)] = neighbours_on_grid

        return tile_adjacency

    def update_adjacency(self):
        for row in range(self.rows):
            for col in range(self.columns):
                neighbours = self.tile_adjacency_map[(row, col)]
                self.contents[row, col].neighbours = self.tile_adjacency_map[(row, col)] = [self.contents[i, j] for i, j
                                                                                            in neighbours]

    def generate_full_neighbourhood_locales(self, locale):
        """
        Generate a list of coordinates representing the full neighborhood of a given locale.

        Args:
            locale (tuple): Coordinates (row, column) of the tile.

        Returns:
            list of tuple[int, int]: List of coordinates representing the full neighborhood.
        """
        i, j = locale

        # get the rows of cells that make up a neighbourhood
        top_row = [(i - 1, col) for col in range(j - 1, j + 2)]
        tile_row = [(i, col) for col in range(j - 1, j + 2)]
        bottom_row = [(i + 1, col) for col in range(j - 1, j + 2)]

        # exclude the tile in question and there you have it
        tile_row.remove(locale)

        neighbourhood = top_row \
                        + tile_row \
                        + bottom_row
        return neighbourhood

    def get_tile_locales(self):
        """
        Get the coordinates of all tiles in the grid.

        Returns:
            list of tuple[int, int]: List of coordinates of all tiles in the grid.
        """

        coords = []
        for row in range(self.rows):
            for col in range(self.columns):
                coords.append((row, col))
        return coords

    def set_tile_locales(self):
        """
        Set the coordinates for each tile in the grid.

        Updates the matrix to include the coordinates for each tile.
        """
        coords = self.get_tile_locales()

        for i, j in coords:
            self.contents[i, j] = (i, j)

    def replace_locale_with_tile_on_grid(self, tile):
        """
        Replace the locale tuple in contents(and all representations of grid items) with the specified tile object.

        Args:
            tile (Tile): Tile object to replace the locale tuple in contents.
        """
        # get index of list containing tuple with tile's coords
        i, j = tile
        self.contents[i, j] = tile







