from pygame import QUIT

from src.game_build.minesweeper import ModeFactory
from src.viewer.button import Button
from src.viewer.constants import *
from src.viewer.view import setUp
from src.viewer.view import fonts
import pygame
import os

project_dir = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]  # Get root directory
images_folder = os.path.join(project_dir, "assets/images")
fonts_folder = os.path.join(project_dir, "assets/fonts")
clips_folder = os.path.join(project_dir, "assets/clips")
sprites_folder = os.path.join(project_dir, "assets/sprite-sheets")

pygame.init()
# Font and color constants
BUTTON_FONT = pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), 35)
FONT = pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), 16)  # Adjust font size as needed
TEXT_COLOR = colours.DARK_SLATE_GREY  # White color for text

LOGO_FONT = pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), 18)  # Adjust font size as needed
MODE_BUTTON_TEXT_COLOR = colours.SLATE_GREY
MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT = 300, 150
icon_w, icon_h = 130, 50

# Help page content (replace with your actual help text)
HELP_CONTENT = [
    "How to Play:",
    "  Starting the Game:",
    "    Click any cell to start. The first cell will never be a bomb.",
    "  Marking Bombs:",
    "    Right-click on a covered cell to place a flag if you suspect a bomb.",
    "  Uncovering Safe Zones:",
    "    Left-click on a covered cell to uncover it. ",
    "If it's safe and has no adjacent bombs, nearby cells will also be uncovered automatically.",
    "  Game Over:",
    "    If you uncover a bomb, all cells will be revealed, and the game will end.",
    "",
    "Use these instructions to navigate the game and understand the mechanics of each action.",
    " Good luck and enjoy playing!"
]

lose_spritesheet = pygame.image.load(os.path.join(sprites_folder, "clipped-lose-sheet.png"))
dupe_sheet = pygame.image.load(os.path.join(sprites_folder, "clipped-lose-sheet.png"))
number_of_frames = 20

frame_width = lose_spritesheet.get_width() // number_of_frames
frame_height = lose_spritesheet.get_height()


class Landing:
    def __init__(self):
        self.tile_size = 150

        self.help_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT, "Help",
                                  pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                                  colours.RED, colours.PINK, colours.CELADON_GREEN, handle_help_click)
        self.choose_board_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT,
                                          "choose board",
                                          pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                                          colours.RED, colours.PINK, colours.CELADON_GREEN, handle_help_click)

    def generate_flagged_tile_image(self, image_path: str, colour_path: str = colours.ASH_GREY):
        size = self.tile_size
        flag_icon = pygame.image.load(os.path.join(images_folder, image_path)).convert_alpha()
        flag_icon = pygame.transform.scale(flag_icon, (size - 5, size - 5))
        flagged_tile_img = pygame.Surface((size, size))
        flagged_tile_img.fill(colour_path)
        return flagged_tile_img, flag_icon

    def generate_revealed_bomb_image(self, image_path: str, colour_path=colours.TOMATO):
        size = self.tile_size
        bomb = pygame.image.load(os.path.join(images_folder, image_path)).convert_alpha()
        bomb = pygame.transform.scale(bomb, (size - 5, size - 5))
        revealed_mine_tile_img = pygame.Surface((size, size))
        revealed_mine_tile_img.fill(colour_path)
        return revealed_mine_tile_img, bomb

    def generate_info_button_image(self, image_path: str):
        size = self.tile_size // 3
        info_image = pygame.image.load(os.path.join(images_folder, image_path)).convert_alpha()
        info_image = pygame.transform.scale(info_image, (size, size))
        return info_image

    def generate_preview_button_image(self, image_path: str):
        size = self.tile_size // 3
        preview_image = pygame.image.load(os.path.join(images_folder, image_path)).convert_alpha()
        preview_image = pygame.transform.scale(preview_image, (size, size))
        return preview_image

    def generate_home_button_image(self, image_path: str):
        size = self.tile_size // 2
        home_image = pygame.image.load(os.path.join(images_folder, image_path)).convert_alpha()
        home_image = pygame.transform.scale(home_image, (size, size))
        return home_image


class Animation:
    def __init__(self, sprite_sheet: pygame.Surface, width, height):
        self.sprite_sheet = sprite_sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.current_frame = 0  # Index of the current frame

    def get_current_frame(self):
        # extract desired frame from sheet
        x = self.current_frame * self.frame_width
        y = 0
        return self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))

    def update(self):
        self.current_frame += 1
        if self.current_frame >= number_of_frames:
            self.current_frame = 0


def generate_home_button_image(image_path: str):
    size = 150 // 2
    home_image = pygame.image.load(os.path.join(images_folder, image_path)).convert_alpha()
    home_image = pygame.transform.scale(home_image, (size, size))
    return home_image


def draw_help_page(screen, home_button):
    """
    This function draws the help page content on the screen.
    """
    screen.fill(colours.WHITE)  # Fill background with black
    idle_home_icon = generate_home_button_image("home(1).png")
    hovered_home_icon = generate_home_button_image("home(2).png")
    home_button.draw_image_button(screen, hovered_home_icon, idle_home_icon)
    # Create text surfaces for each line of help content
    text_surfaces = []
    for line in HELP_CONTENT:
        text_surface = FONT.render(line, True, TEXT_COLOR)
        text_surfaces.append(text_surface)

    # Calculate starting position for the first line of text
    y_pos = 20  # Adjust top margin

    # Draw each line of text with spacing
    for text_surface in text_surfaces:
        screen.blit(text_surface, (10, y_pos))  # Adjust left margin
        y_pos += text_surface.get_height() + 5  # Add spacing between lines


def draw_home_button(screen, home_button):
    idle_home_icon = generate_home_button_image("home(1).png")
    hovered_home_icon = generate_home_button_image("home(2).png")
    home_button.draw_image_button(screen, hovered_home_icon, idle_home_icon)

def draw_preview_scrolls():
    size = 150 // 2
    image_path = "clipped-win.png"
    win_image = pygame.image.load(os.path.join(images_folder, image_path)).convert_alpha()
    win_image = pygame.transform.scale(win_image, (size, size))


def draw_preview_window():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SCALED | pygame.DOUBLEBUF, vsync=2)
    screen.fill(colours.CELADON_GREEN)
    pygame.display.set_caption("game play preview")
    clock = pygame.time.Clock()

    # Create animation instance
    animation = Animation(lose_spritesheet, frame_width, frame_height)

    home_button = Button(90, WINDOW_HEIGHT - 100, 100, 100, ".",
                         pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                         colours.THISTLE, colours.THISTLE, colours.CELADON_GREEN, draw_preview_window,
                         "Returns to main page")
    scroll_left = Button(90, WINDOW_HEIGHT - 100, 100, 100, ".",
                         pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                         colours.THISTLE, colours.THISTLE, colours.CELADON_GREEN, draw_preview_window,
                         "see previous item")

    scroll_right = Button(90, WINDOW_HEIGHT - 100, 100, 100, ".",
                          pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                          colours.THISTLE, colours.THISTLE, colours.CELADON_GREEN, draw_preview_window,
                          "see next item")

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if home_button.is_clicked(pos):
                    return main()

        draw_home_button(screen, home_button)
        animation.update()

        # Get current frame surface
        current_frame = animation.get_current_frame()

        # Draw the frame onto the screen at a specific position
        screen.blit(current_frame, (100, 100))

        # Update the display
        pygame.display.flip()

        # Set frame rate (adjust as needed)
        clock.tick(10)  # Aim for 30 FPS

    # Quit Pygame
    pygame.quit()


def handle_help_click():
    """
    This function creates a new surface for the help window and displays the help content.
    """
    help_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SCALED | pygame.DOUBLEBUF,
                                          vsync=2)
    pygame.display.set_caption("Minesweeper Help")

    home_button = Button(90, WINDOW_HEIGHT - 100, 100, 100, ".",
                         pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                         colours.THISTLE, colours.THISTLE, colours.CELADON_GREEN, handle_help_click,
                         "Returns to main page")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if home_button.is_clicked(pos):
                    return main()

        draw_help_page(help_window, home_button)
        pygame.display.flip()
        pygame.time.Clock().tick(500)

    # Clean up the help window after closing
    pygame.display.quit()


def create_rounded_rectangle(width, height, radius, colour):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    pygame.draw.rect(surface, colour, (0, 0, width, height), border_radius=radius)
    return surface


def draw_mode_buttons(buttons, screen):
    for button in buttons.values():
        button.draw_mode_button(screen)


def draw_selection_page():
    home_button = Button(420, WINDOW_HEIGHT - 100, 100, 100, ".",
                         pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                         colours.THISTLE, colours.THISTLE, colours.CELADON_GREEN, draw_selection_page,
                         "Returns to main page")

    selection_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SCALED | pygame.DOUBLEBUF,
                                               vsync=2)
    selection_window.fill(colours.SNOW)
    pygame.display.set_caption("board selection window")
    clock = pygame.time.Clock()

    easy_x, easy_y = 100, 33
    white_space = 40
    # create the buttons for the different board sizes
    EASY = Button(easy_x, easy_y, MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT, "", LOGO_FONT, colours.ASH_GREY,
                  colours.ASH_GREY, colours.ASH_GREY,
                  draw_selection_page)
    EASY.mode = ModeFactory().generate_preset_mode("easy")
    MEDIUM = Button(easy_x, easy_y + MODE_BUTTON_HEIGHT + white_space, MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT, "",
                    LOGO_FONT, colours.ASH_GREY,
                    colours.ASH_GREY, colours.ASH_GREY, draw_selection_page)
    MEDIUM.mode = ModeFactory().generate_preset_mode("medium")
    HARD = Button(easy_x, easy_y + 2 * white_space + (2 * MODE_BUTTON_HEIGHT), MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT,
                  "", LOGO_FONT,
                  colours.ASH_GREY,
                  colours.ASH_GREY, colours.ASH_GREY, draw_selection_page)
    HARD.mode = ModeFactory().generate_preset_mode("hard")

    buttons = {"easy": EASY, "medium": MEDIUM, "hard": HARD}
    for name, b in buttons.items():
        b.mode_font = LOGO_FONT.render(name.upper(), True, (0, 0, 0))
    running = True
    while running:
        draw_mode_buttons(buttons, selection_window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons.values():
                    if button.is_clicked(pos):
                        return main(button.mode)
                    if home_button.is_clicked(pos):
                        return main()

        draw_home_button(selection_window, home_button)
        # update the screen
        pygame.display.flip()
        clock.tick(500)

    pygame.quit()


def main(game=None):
    if game:
        setUp(game)
        return
    # setup main window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SCALED | pygame.DOUBLEBUF, vsync=2)
    window.fill(colours.banner)
    pygame.display.set_caption("Minesweeper Help")
    banner = pygame.image.load(os.path.join(images_folder, "detailed-banner.png"))
    # banner = pygame.transform.scale(banner, (WINDOW_WIDTH, 270))
    window.blit(banner, (60, 60))
    # create help button
    help_button = Button(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2 + 30, 200, 40, "Best Times",
                         pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 24),
                         colours.ORANGE, colours.PINK, colours.CELADON_GREEN, handle_help_click)

    choose_board_button = Button(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2 + 100, 200, 40,
                                 "choose board",
                                 pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), 24),
                                 colours.RED, colours.PINK, colours.CELADON_GREEN, handle_help_click)

    info_button = Button(460, WINDOW_HEIGHT // 2 + 30, 51, 51, ".",
                         pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                         colours.banner, colours.banner, colours.CELADON_GREEN, handle_help_click,
                         "Help info and strategy")

    preview_button = Button(460, WINDOW_HEIGHT // 2 + 100, 51, 51, ".",
                            pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                            colours.banner, colours.banner, colours.CELADON_GREEN, handle_help_click,
                            "Game play visuals")

    home_button = Button(0, 0, 100, 100, ".",
                         pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                         colours.WHITE, colours.WHITE, colours.CELADON_GREEN, handle_help_click,
                         "Returns to main page")

    # initialise landing
    landing = Landing()

    idle_info_icon = landing.generate_info_button_image("information.png")
    hovered_info_icon = landing.generate_info_button_image("information(1).png")
    idle_preview = landing.generate_preview_button_image("eyebrow.png")
    hovered_preview = landing.generate_preview_button_image("visibility.png")
    # load the
    while True:
        help_button.draw(window)
        choose_board_button.draw(window)
        info_button.draw_image_button(window, hovered_info_icon, idle_info_icon)
        preview_button.draw_image_button(window, hovered_preview, idle_preview)

        # Check for button clicks
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if help_button.is_clicked(pos):
                    handle_help_click()
                elif choose_board_button.is_clicked(pos):
                    draw_selection_page()
                elif info_button.is_clicked(pos):
                    handle_help_click()
                elif preview_button.is_clicked(pos):
                    draw_preview_window()
            elif event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()
        pygame.time.Clock().tick(100)

# todo: cleanup time via bdd

# todo landing page story: help
#   As a player
#   I want a quick intro into the core gameplay and strategies
#   So that I can understand the basics of the game before playing

#  todo landing page: board selection
#   As a player
#   I want to be presented with the different difficulty levels available
#   So that I can choose a difficulty that suits my interests

#  todo landing page: aesthetics and UX
#   As a player
#   I want to see a visually appealing welcome
#   So that I can get a sense and feel of the game

#  todo landing page: easy start
#   As a player
#   I want to easily start playing the game
#   So that I don't have to wait for the landing page to load the game

# todo landing on the page:
#     Given a user arrives at the Minesweeper game landing page.
#     When the page loads,
#     Then it should display a help button
#     And this should display a clear and concise explanation of the game's objective
#     (uncovering tiles while avoiding mines).
#     And it should showcase the different difficulty levels (e.g., easy, medium, hard)
#     with brief descriptions of each (e.g., board size, mine count).

# todo difficulty level selection:
#     Given a user clicks on a difficulty level button (e.g., "Easy").
#     When the user selects a difficulty level.
#     Then the controller should capture this selection
#     And relay it to the model
#     And the game should be launched with the corresponding board size and mine count pre-configured.

# todo: viewing the game interface:
#     Given the user is on the landing page.
#     When the user scrolls down or clicks a "See the Game" button (optional).
#     Then a section should be revealed showcasing a static image or animated GIF of the game interface.
#     And this should highlight key elements like the board, tiles, flags, and timer (if applicable).

# todo starting the game:
#     Given the user is ready to play.
#     When the user clicks a "Start Game" button.
#     Then the game should launch with the chosen difficulty level (or default settings).
