from pygame import QUIT

from button import Button as better
from constants import *
import fonts
import pygame

pygame.init()
# Font and color constants
BUTTON_FONT = pygame.font.Font(fonts.GEOLOGICA, 35)
FONT = pygame.font.Font(fonts.GEOLOGICA, 24)  # Adjust font size as needed
TEXT_COLOR = (255, 255, 255)  # White color for text

# Help page content (replace with your actual help text)
HELP_CONTENT = [
    "Welcome to Minesweeper!",
    "Click to reveal tiles. Numbers indicate surrounding mines.",
    "Right-click to place flags on suspected mines.",
    "Avoid mines to win!",
    "Click 'X' or the top right corner to close this window.",
]


class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback  # Function to call on click

    def draw(self, screen, font=BUTTON_FONT, color=(200, 200, 200), text_color=(0, 0, 0)):
        # Draw button rectangle
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        # Draw button text (optional)
        if font:
            text_surface = font.render(self.text, True, text_color)
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


class Landing:
    def __init__(self):
        self.tile_size = 150

        self.help_button = better(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT, "Help",
                                  pygame.font.Font(fonts.ROBOTO, 30),
                                  colours.RED, colours.PINK, colours.CELADON_GREEN, handle_help_click)
        # self.mode_button = pygame.Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT, "Choose Board",
        #                             handle_mode_click)

    def generate_flagged_tile_image(self, image_path: str, colour_path: str = colours.ASH_GREY):
        size = self.tile_size
        flag_icon = pygame.image.load(image_path).convert_alpha()
        flag_icon = pygame.transform.scale(flag_icon, (size - 5, size - 5))
        flagged_tile_img = pygame.Surface((size, size))
        flagged_tile_img.fill(colour_path)
        return flagged_tile_img, flag_icon

    def generate_revealed_bomb_image(self, image_path: str, colour_path=colours.TOMATO):
        size = self.tile_size
        bomb = pygame.image.load(image_path).convert_alpha()
        bomb = pygame.transform.scale(bomb, (size - 5, size - 5))
        revealed_mine_tile_img = pygame.Surface((size, size))
        revealed_mine_tile_img.fill(colour_path)
        return revealed_mine_tile_img, bomb


# mode_button = pygame.Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT, "Choose Board",
#                                     handle_mode_click)

def draw_help_page(screen):
    """
    This function draws the help page content on the screen.
    """
    screen.fill((0, 0, 0))  # Fill background with black

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

    # Optional: Add a close button (replace with your button handling logic)
    # close_button = Button(screen_width - 50, 10, 40, 20, "X", handle_close_click)
    # close_button.draw(screen)


def handle_help_click():
    """
    This function creates a new surface for the help window and displays the help content.
    """
    help_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    help_window.fill(colours.THISTLE)
    pygame.display.set_caption("Minesweeper Help")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if close_button.is_clicked(event.pos):
            #         running = False

        draw_help_page(help_window)
        pygame.display.flip()

    # Clean up the help window after closing
    pygame.display.quit()


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill(colours.WHITE)
pygame.display.set_caption("Minesweeper Help")
help_button = better(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 120, 120, "Help",
                     pygame.font.Font(fonts.ROBOTO, 30),
                     colours.RED, colours.PINK, colours.CELADON_GREEN, handle_help_click)

landing = Landing()
flag_surface, flag_icon = landing.generate_flagged_tile_image("flag.png", colours.SLATE_GREY)
flag_icon = pygame.transform.rotate(flag_icon, 45)
mine_surface, mine_icon = landing.generate_revealed_bomb_image("spikes.png", colours.SLATE_GREY)
window.blit(flag_surface, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4))
window.blit(flag_icon, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4))
window.blit(mine_surface, (WINDOW_WIDTH * 0.8, WINDOW_HEIGHT * 0.8))
window.blit(mine_icon, (WINDOW_WIDTH * 0.7, WINDOW_HEIGHT * 0.7))
flag_surface, flag_icon = landing.generate_flagged_tile_image("grey.png", colours.BEIGE)
flag_icon = pygame.transform.rotate(flag_icon, 45)
window.blit(flag_surface, (WINDOW_WIDTH * 0.8, WINDOW_HEIGHT // 4))
window.blit(flag_icon, (WINDOW_WIDTH * 0.8, WINDOW_HEIGHT // 4))
while True:
    help_button.draw(window)

    # Check for button clicks
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if help_button.is_clicked(pos):
                handle_help_click()
        elif event.type == QUIT:
            pygame.quit()
    pygame.display.flip()
    pygame.time.Clock().tick(3)
