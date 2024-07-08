import pygame
import os
from src.game_build.minesweeper import Mode, ModeFactory
from src.viewer.constants import *
from src.viewer.colours import *
from src.viewer.button import Button
from src.viewer import fonts
from src.viewer.utils import generate_home_button_image
from src.viewer.landing import main as launch

project_dir = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]  # Get root directory
images_folder = os.path.join(project_dir, "assets/images")
fonts_folder = os.path.join(project_dir, "assets/fonts")

pygame.init()
LOGO_FONT = pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), 18)  # Adjust font size as needed
MODE_BUTTON_TEXT_COLOR = colours.SLATE_GREY
MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT = 300, 150
icon_w, icon_h = 130, 50


def handler():
    pass


# def generate_mine_count_surface(self):
#     mine_count_image = pygame.Surface((icon_w, icon_h))
#     mine_count_image.fill(ASH_GREY)
#
#     mine = pygame.image.load(os.path.join(images_folder, "mine-detonated.png")).convert_alpha()
#     mine = pygame.transform.scale(mine, (icon_h, icon_h))
#
#     mine_count_image.blit(mine, (0, 0))
#     count_image = LOGO_FONT.render(str(self.mode.mine_count), True, BLACK)
#     mine_count_image.blit(count_image, (icon_h + 7, 0))
#     return mine_count_image
#
#
# def generate_grid_size_surface(self):
#     grid_size_info = pygame.Surface((icon_w, icon_h))
#     grid_size_info.fill(ASH_GREY)
#
#     grid_img = pygame.image.load(os.path.join(images_folder, "pixels.png")).convert_alpha()
#     grid_img = pygame.transform.scale(grid_img, (icon_h, icon_h))
#
#     grid_size_info.blit(grid_img, (0, 0))
#     count_image = LOGO_FONT.render(str(self.mode.size) + " x " + str(self.mode.size), True, BLACK)
#     grid_size_info.blit(count_image, (icon_h + 12, 0))
#     return grid_size_info


def draw_home_button(screen, home_button):
    idle_home_icon = generate_home_button_image("home(1).png")
    hovered_home_icon = generate_home_button_image("home(2).png")
    home_button.draw_image_button(screen, hovered_home_icon, idle_home_icon)


def draw_mode_buttons(buttons, screen):
    for button in buttons.values():
        button.draw_mode_button(screen)


def draw_selection_page():
    home_button = Button(90, WINDOW_HEIGHT - 100, 100, 100, ".",
                         pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                         colours.THISTLE, colours.THISTLE, colours.CELADON_GREEN, launch,
                         "Returns to main page")

    selection_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SCALED, vsync=2)
    selection_window.fill(SNOW)
    pygame.display.set_caption("board selection window")
    clock = pygame.time.Clock()

    easy_x, easy_y = 100, 33
    white_space = 40
    # create the buttons for the different board sizes
    EASY = Button(easy_x, easy_y, MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT, "", LOGO_FONT, ASH_GREY, ASH_GREY, YELLOW,
                  handler)
    EASY.mode = ModeFactory().generate_preset_mode("easy")
    MEDIUM = Button(easy_x, easy_y + MODE_BUTTON_HEIGHT + white_space, MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT, "",
                    LOGO_FONT, ASH_GREY,
                    ASH_GREY, YELLOW, handler)
    MEDIUM.mode = ModeFactory().generate_preset_mode("medium")
    HARD = Button(easy_x, easy_y + 2 * white_space + (2 * MODE_BUTTON_HEIGHT), MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT,
                  "", LOGO_FONT,
                  ASH_GREY,
                  ASH_GREY, YELLOW, handler)
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
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     pass
            #     pos = pygame.mouse.get_pos()
            #     if EASY.is_clicked(pos):
            #         return main()

        draw_home_button(selection_window, home_button)
        # update the screen
        pygame.display.flip()
        clock.tick(100)

    pygame.quit()


if __name__ == "__main__":
    draw_selection_page()
