import json
import os
import sys
import time
from random import choice

import pygame

from src.game_build.minesweeper import Board, Game, Mode, ModeFactory
from src.game_build.tile import SafeTile
from src.viewer import colours, fonts, constants
from src.viewer import confetti as visuals
from src.viewer.button import Button

project_dir = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0] # Get project directory
images_folder = os.path.join(project_dir, "assets/images")  # Path to viewer folder
fonts_folder = os.path.join(project_dir, "assets/fonts")

class View:
    # brings up landing page
    # allows user to navigate the pages
    # board selection page leads to triggering the controller
    pass

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
FPS = 30

# Define overall window dimensions
WINDOW_WIDTH = constants.WINDOW_WIDTH
WINDOW_HEIGHT = constants.WINDOW_HEIGHT

# Define grid dimensions and position within the window
GRID_WIDTH = 540
GRID_HEIGHT = 540
GRID_TOP_LEFT_X = (WINDOW_WIDTH - GRID_WIDTH - 20)
GRID_TOP_LEFT_Y = (WINDOW_HEIGHT - GRID_HEIGHT) // 2

print((GRID_TOP_LEFT_X, GRID_TOP_LEFT_Y))
print((GRID_TOP_LEFT_X + GRID_WIDTH, GRID_TOP_LEFT_Y + GRID_HEIGHT))

# Set up the Pygame screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper")
screen.fill(colours.CELADON_GREEN)

# Load the icon image
icon_image = pygame.image.load(os.path.join(images_folder, "mine-detonated.png")).convert_alpha()
icon_image = pygame.transform.scale(icon_image, (32, 32))

# Set the window icon
pygame.display.set_icon(icon_image)

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

confetti = visuals.create_confetti(850)


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
    numbers_font = pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), size - 5)
    number_images = [numbers_font.render(str(mine_count), True, colours.BLACK) for mine_count in range(1, 9)]

    # Create surfaces for different tile states
    unrevealed_tile_img = pygame.Surface((size, size))
    unrevealed_tile_img.fill(colours.ASH_GREY)

    flag = pygame.image.load(os.path.join(images_folder, "grey.png")).convert_alpha()
    flag = pygame.transform.scale(flag, (size - 5, size - 5))
    flagged_tile_img = pygame.Surface((size, size))

    revealed_tile_blank_img = pygame.Surface((size, size))
    revealed_tile_blank_img.fill(colours.CARAMEL)

    bomb = pygame.image.load(os.path.join(images_folder, "mine-custom.png")).convert_alpha()
    bomb = pygame.transform.scale(bomb, (size - 5, size - 5))
    revealed_mine_tile_img = pygame.Surface((size, size))

    detonated_bomb = pygame.image.load(os.path.join(images_folder, "mine-detonated.png")).convert_alpha()
    detonated_bomb = pygame.transform.scale(detonated_bomb, (size - 5, size - 5))
    revealed_detonated_mine_tile_img = pygame.Surface((size, size))

    outcome = read_json()

    # Iterate through each tile in the board and draw it within the grid area
    for row in range(rows):
        for col in range(columns):
            tile = board.get_tile_from_locale((row, col))
            # check json file for events at this location
            # set event status, i think we need an enum!! enum outcome = {Win, Lose, Play}
            x = GRID_TOP_LEFT_X + col * size
            y = GRID_TOP_LEFT_Y + row * size
            pygame.draw.rect(screen, colours.SLATE_GREY, (x - 2, y - 2, size + 2 * 2, size + 2 * 2), 2)

            # Determine how to draw the tile based on its type and state
            if isinstance(tile, tuple):
                screen.blit(unrevealed_tile_img, (x, y))
            else:
                if not tile.is_revealed:
                    if tile.is_flagged:
                        flag_x = size * x // 2 - (size * x - 5) // 2
                        flag_y = size * y // 2 - (size * y - 5) // 2
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
                        bomb_x = size * x // 2 - (size * x - 5) // 2
                        bomb_y = size * y // 2 - (size * y - 5) // 2

                        # update revealed mine tile with image
                        colour = choice([colours.BEIGE, colours.RED])
                        revealed_mine_tile_img.fill(colour)
                        loss_sequence = check_for_special_event(row, col, outcome, event_kind="lose")
                        if not loss_sequence:
                            revealed_mine_tile_img.blit(bomb, (bomb_x, bomb_y))
                            screen.blit(revealed_mine_tile_img, (x, y))
                        else:
                            # print(outcome)
                            revealed_detonated_mine_tile_img.fill(colours.BEIGE)
                            revealed_detonated_mine_tile_img.blit(detonated_bomb, (bomb_x, bomb_y))
                            screen.blit(revealed_detonated_mine_tile_img, (x, y))
                            print("tile at", tuple(outcome["tile"]), "set it off")

    # pygame.display.flip()
    # clock.tick(FPS)


def read_json() -> dict:
    # Load data from a JSON file
    with open("this_round.json", 'r') as json_file:
        outcome = json.load(json_file)
    return outcome if outcome else {}


def check_for_special_event(row, col, outcome, event_kind="win"):
    is_event = outcome["outcome"] == event_kind
    special = (row, col) == tuple(outcome["tile"])
    return is_event and special


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


def draw_window(game: Game, elapsed_time: int):
    """
    Draws the main window with the Minesweeper board centered within the designated grid area.

    Args:
    - board: The Minesweeper board object to draw.
    """
    global confetti
    screen.fill(colours.CELADON_GREEN)
    update_flags(game)
    track_time(game, elapsed_time)
    change_mode()
    draw_board(game.get_game_board())
    # win

    outcome = read_json()
    is_win = outcome.get("outcome") == "win"
    is_lose = outcome.get("outcome") == "lose"
    second_batch = []
    # if all(atom.y + 50 >= WINDOW_HEIGHT//2 for atom in confetti):  # remake confetti if they've all disappeared
    #     second_batch = visuals.create_confetti(850)

    if all(atom.y + 50 >= WINDOW_HEIGHT for atom in confetti):  # remake confetti if they've all disappeared
        confetti = visuals.create_confetti(850)
    if is_win:
        throw_confetti(screen, confetti)
        throw_confetti(screen, second_batch)
        win_image_paths = ["viewer/win-purple.png", "viewer/win-green.png", "viewer/win-pink.png",
                           "viewer/win-purple.png", "viewer/win-green.png", "viewer/win-pink.png"]
        win_image_path = choice(win_image_paths)
        win_image = pygame.image.load(os.path.join(images_folder, "win-green.png")).convert_alpha()
        win_image = pygame.transform.scale(win_image, (150, 150))
        screen.blit(win_image, (GRID_TOP_LEFT_X - 156, WINDOW_HEIGHT // 2 - 60))
    elif is_lose:
        loser_img_path = os.path.join(images_folder, "loser.png")
        loser_img = pygame.image.load(loser_img_path).convert_alpha()
        loser_img = pygame.transform.scale(loser_img, (150, 150))
        screen.blit(loser_img, (GRID_TOP_LEFT_X - 150, WINDOW_HEIGHT // 2 - 60))
    pygame.display.flip()
    clock.tick(FPS)


def close():
    """
    Closes the Pygame window and exits the program.
    """
    pygame.quit()
    sys.exit()

def setUp(mode):
    sys.setrecursionlimit(10 ** 6)
    # Create Board instance
    board1 = Board(mode)

    # Create Game instance
    minesweeper = Game(board1)
    main(minesweeper)

def main(minesweeper: Game):
    """
    Main function to initialize the game and handle game loop.
    """

    start_time = None
    game_duration = 0
    running = True
    confetti = visuals.create_confetti(850)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                print(mouse_position)
                is_play = click_is_on_grid(mouse_position)
                print(is_play)
                if is_play:
                    try:
                        selected_tile = get_grid_location_of_tile(mouse_position, minesweeper.get_game_board())
                        tile = minesweeper.get_game_board().get_tile_from_locale(selected_tile)
                    except TypeError:
                        continue
                    if isinstance(tile, tuple):
                        start_time = time.time()  # start the timer on first button click
                        minesweeper.setup(selected_tile)
                        continue
                    elif not minesweeper.is_in_play():
                        continue
                    flag = event.button == 3
                    minesweeper.handle_selection(selected_tile, flag)
        elapsed_time = 0 if start_time is None else int(time.time() - start_time)  # set it to none and then use ternary
        if minesweeper.is_in_play():
            game_duration = elapsed_time
        draw_window(minesweeper, game_duration)

    close()


def throw_confetti(screen_parm, confetti):
    for atom in confetti:
        atom.update()
        atom.draw(screen_parm)


def update_flags(game: Game):
    flag = pygame.image.load(os.path.join(images_folder, "grey.png")).convert_alpha()
    flag = pygame.transform.scale(flag, (32, 32))

    flags_font = pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), 20)
    flags_placed_img = flags_font.render(str(game.get_number_of_flags_placed()) + "/" + str(game.get_mine_count()),
                                         True, colours.BLACK)
    flag_progress = pygame.Surface((50, 50))
    flag_progress.fill(colours.LIGHT_GREY)
    screen.blit(flag, (GRID_TOP_LEFT_X - 50 * 2 + 15, 50))
    screen.blit(flags_placed_img, (GRID_TOP_LEFT_X - 50 * 2, GRID_TOP_LEFT_X - 65))


def track_time(game: Game, elapsed_time: int):
    clock_icon = pygame.image.load(os.path.join(images_folder, "clock.png")).convert_alpha()
    clock_icon = pygame.transform.scale(clock_icon, (50, 50))
    screen.blit(clock_icon, (GRID_TOP_LEFT_X - 50 * 2, 150))

    timer_font = pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), 20)
    timer_img = timer_font.render(f"{elapsed_time // 60:02}:{elapsed_time % 60:02}", True, colours.BLACK)
    screen.blit(timer_img, (GRID_TOP_LEFT_X - 50 * 3 + 45, 200))


def change_mode():
    mode_screen = None
    mode_button = Button(GRID_TOP_LEFT_X - 150, WINDOW_HEIGHT * 0.8, 120, 32, "mode",
                         pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), 30),
                         colours.YELLOW, colours.ORANGE, colours.CELADON_GREEN, mode_screen)

    mode_button.draw(screen)


def click_is_on_grid(click_position: tuple):
    click_x, click_y = click_position
    bottom_right = GRID_TOP_LEFT_X + GRID_WIDTH, GRID_TOP_LEFT_Y + GRID_HEIGHT
    within_top = click_y >= GRID_TOP_LEFT_Y
    within_bottom = click_y <= bottom_right[-1]
    within_left = click_x >= GRID_TOP_LEFT_X
    within_right = click_x <= bottom_right[0]
    return within_top and within_bottom and within_right and within_left
