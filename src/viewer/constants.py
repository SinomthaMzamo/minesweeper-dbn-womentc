import colours
# Define overall window dimensions
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 600

# Define grid dimensions and position within the window
GRID_WIDTH = 540
GRID_HEIGHT = 540
GRID_TOP_LEFT_X = (WINDOW_WIDTH - GRID_WIDTH-20)
GRID_TOP_LEFT_Y = (WINDOW_HEIGHT - GRID_HEIGHT) // 2

# Colour map for numbers on tiles
colour_map = {
    0: colours.ASH_GREY,
    1: colours.THISTLE,
    2: colours.CELADON_GREEN,
    3: colours.PINK,
    4: colours.LIGHT_ORANGE,
    5: colours.TOMATO,
    6: colours.DEEP_SKY_BLUE,
    7: colours.PALE_YELLOW,
    8: colours.RED
}