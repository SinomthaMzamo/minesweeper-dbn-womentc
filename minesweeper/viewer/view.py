import pygame
from random import choice
from game_build.minesweeper import Board, Game
from game_build.tile import SafeTile
import sys
import colours
import fonts

# Initialize Pygame
pygame.init()

# Define overall window dimensions
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 600

# Define grid dimensions and position within the window
GRID_WIDTH = 540
GRID_HEIGHT = 540
GRID_TOP_LEFT_X = (WINDOW_WIDTH - GRID_WIDTH-20)
GRID_TOP_LEFT_Y = (WINDOW_HEIGHT - GRID_HEIGHT) // 2

print((GRID_TOP_LEFT_X,GRID_TOP_LEFT_Y))
print((GRID_TOP_LEFT_X+GRID_WIDTH, GRID_TOP_LEFT_Y+GRID_HEIGHT))

# Set up the Pygame screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper")

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


def draw_board(board: Board):
    """
    Draws the Minesweeper board within the designated grid area of the Pygame screen.

    Args:
    - board (Board): The Minesweeper board object containing tile information.
    """
    # Extract board dimensions
    rows = board.get_rows()
    columns = board.get_columns()
    size = min(GRID_WIDTH // columns, GRID_HEIGHT // rows)  # Adjust size to fit grid area

    # Prepare number images for tiles
    numbers_font = pygame.font.Font(fonts.GEOLOGICA, size - 5)
    number_images = [numbers_font.render(str(mine_count), True, colours.BLACK) for mine_count in range(1, 9)]

    # Create surfaces for different tile states
    unrevealed_tile_img = pygame.Surface((size, size))
    unrevealed_tile_img.fill(colours.ASH_GREY)

    flag = pygame.image.load("grey.png").convert_alpha()
    flag = pygame.transform.scale(flag, (size - 5, size - 5))
    flagged_tile_img = pygame.Surface((size, size))

    revealed_tile_blank_img = pygame.Surface((size, size))
    revealed_tile_blank_img.fill(colours.CARAMEL)

    bomb = pygame.image.load("simple_bomb.png").convert_alpha()
    bomb = pygame.transform.scale(bomb, (size - 10, size - 10))
    revealed_mine_tile_img = pygame.Surface((size, size))


    # Iterate through each tile in the board and draw it within the grid area
    for row in range(rows):
        for col in range(columns):
            tile = board.get_tile_from_locale((row, col))
            x = GRID_TOP_LEFT_X + col * size
            y = GRID_TOP_LEFT_Y + row * size
            pygame.draw.rect(screen, colours.SLATE_GREY, (x - 2, y - 2, size + 2 * 2, size + 2 * 2), 2)

            # Determine how to draw the tile based on its type and state
            if isinstance(tile, tuple):
                screen.blit(unrevealed_tile_img, (x, y))
            else:
                if not tile.is_revealed:
                    if tile.is_flagged:
                        flag_x = size*x//2 - (size*x - 5) // 2
                        flag_y = size*y//2 - (size*y - 5) // 2
                        flagged_tile_img.fill(colours.ASH_GREY)
                        flagged_tile_img.blit(flag, (flag_x, flag_y))
                        screen.blit(flagged_tile_img, (x, y))
                    else:
                        screen.blit(unrevealed_tile_img, (x, y))
                else:
                    if isinstance(tile, SafeTile):
                        mine_count = tile.count_neighbourhood_mines()
                        if mine_count > 0:
                            revealed_tile_blank_img.fill(colour_map[mine_count])
                            screen.blit(revealed_tile_blank_img, (x, y))
                            screen.blit(number_images[mine_count - 1], (x, y))
                        else:
                            revealed_tile_blank_img.fill(colours.BEIGE)
                            screen.blit(revealed_tile_blank_img, (x, y))
                    else:
                        # find image centre
                        bomb_x = size * x // 2 - (size * x - 10) // 2
                        bomb_y = size * y // 2 - (size * y - 5) // 2
                        # update revealed mine tile with image
                        revealed_mine_tile_img.fill(colours.SALMON)
                        revealed_mine_tile_img.blit(bomb, (bomb_x, bomb_y))
                        screen.blit(revealed_mine_tile_img, (x, y))
    pygame.display.flip()


def get_grid_location_of_tile(mouse_click_location: tuple, board: Board):
    """
    Determines the grid location (row, column) of a tile based on mouse click position within the grid area.

    Args:
    - mouse_click_location (tuple): Tuple containing x, y coordinates of the mouse click.
    - board (Board): The Minesweeper board object.

    Returns:
    - tuple: Coordinates (row, column) of the clicked tile within the board.
    """
    # Convert mouse click coordinates to grid coordinates within the board
    relative_x = mouse_click_location[0] - GRID_TOP_LEFT_X
    relative_y = mouse_click_location[1] - GRID_TOP_LEFT_Y

    tile_location_x = relative_x // (GRID_WIDTH // board.get_columns())
    tile_location_y = relative_y // (GRID_HEIGHT // board.get_rows())

    # Ensure the clicked location is within valid board bounds
    if (0 <= tile_location_x < board.get_columns()
            and 0 <= tile_location_y < board.get_rows()):
        return tile_location_y, tile_location_x


def draw_window(game: Game):
    """
    Draws the main window with the Minesweeper board centered within the designated grid area.

    Args:
    - board: The Minesweeper board object to draw.
    """
    screen.fill(colours.SNOW)
    update_flags(game)
    track_time(game)
    draw_board(game.get_game_board())
    pygame.display.update()


def close():
    """
    Closes the Pygame window and exits the program.
    """
    pygame.quit()
    sys.exit()


def main():
    """
    Main function to initialize the game and handle game loop.
    """
    # Available game modes
    game_modes = ["easy", "medium", "hard"]
    mode = choice(game_modes)

    # Create Board instance
    board1 = Board("EASY")

    # Create Game instance
    minesweeper = Game(board1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                print(mouse_position)
                is_play = click_is_on_grid(mouse_position)
                print(is_play)
                if is_play :
                    selected_tile = get_grid_location_of_tile(mouse_position, minesweeper.get_game_board())
                    tile = minesweeper.get_game_board().get_tile_from_locale(selected_tile)
                    if isinstance(tile, tuple):
                        minesweeper.board.set_up_game_board(selected_tile)
                        continue
                    flag = event.button == 3
                    minesweeper.run_game(selected_tile, flag)

        draw_window(minesweeper)

    close()

def update_flags(game: Game):
    flag = pygame.image.load("grey.png").convert_alpha()
    flag = pygame.transform.scale(flag, (32, 32))

    flags_font = pygame.font.Font(fonts.GEOLOGICA, 20)
    flags_placed_img = flags_font.render(str(game.get_number_of_flags_placed())+"/"+str(game.get_mine_count()), True, colours.BLACK)
    flag_progress = pygame.Surface((50, 50))
    flag_progress.fill(colours.LIGHT_GREY)
    screen.blit(flag, (GRID_TOP_LEFT_X-50*2+15, 50))
    screen.blit(flags_placed_img, (GRID_TOP_LEFT_X-50*2, GRID_TOP_LEFT_X-65))

def track_time(game: Game):
    clock = pygame.image.load("clock.png").convert_alpha()
    clock = pygame.transform.scale(clock, (50,50))
    screen.blit(clock, (GRID_TOP_LEFT_X-50*2+5, 150))

def click_is_on_grid(click_position: tuple):
    click_x, click_y = click_position
    bottom_right = GRID_TOP_LEFT_X+GRID_WIDTH, GRID_TOP_LEFT_Y+GRID_HEIGHT
    within_top = click_y >= GRID_TOP_LEFT_Y
    within_bottom = click_y <= bottom_right[-1]
    within_left = click_x >= GRID_TOP_LEFT_X
    within_right = click_x <= bottom_right[0]
    return within_top and within_bottom and within_right and within_left

# (432, 30) -> (982, 570)
if __name__ == "__main__":
    main()
