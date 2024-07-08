import pygame
import os
from src.viewer import fonts
from src.game_build.minesweeper import Mode
from src.viewer.colours import *
from src.viewer import colours

project_dir = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]  # Get project directory
images_folder = os.path.join(project_dir, "assets/images")  # Path to viewer folder
fonts_folder = os.path.join(project_dir, "assets/fonts")
pygame.init()

LOGO_FONT = pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), 18)  # Adjust font size as needed
MODE_BUTTON_TEXT_COLOR = colours.SLATE_GREY
MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT = 300, 150

icon_w, icon_h = 130, 50


def create_rounded_rectangle(width, height, radius, colour):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    pygame.draw.rect(surface, colour, (0, 0, width, height), border_radius=radius)
    return surface


class Button:

    def __init__(self, x, y, width, height, text, font, idle_color, hover_color, click_color, click_func, info_text=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.click_func = click_func
        self.surface = create_rounded_rectangle(width, height, int(max(width, height) * 0.1), idle_color)
        self.text_render = font.render(text, True, (0, 0, 0))  # Pre-render text for efficiency
        self.info_text_font = pygame.font.Font(os.path.join(fonts_folder, fonts.GEOLOGICA), 20)  # Adjust font size
        self.info_message = info_text
        self.mode = None
        self.mode_font = None
        self.info_text_colour = colours.DARK_GREY
        self.info_text = self.info_text_font.render(info_text, True, self.info_text_colour)  # Render text

    def hide_info_text(self):
        self.info_text_colour = colours.banner
        self.info_text = self.info_text_font.render(self.info_message, True, self.info_text_colour)  # Render text

    def show_info_text(self):
        self.info_text_colour = colours.DARK_GREY
        self.info_text = self.info_text_font.render(self.info_message, True, self.info_text_colour)  # Render text

    def draw(self, screen):
        self.check_state()  # Update button state based on mouse interaction
        screen.blit(self.surface, (self.x, self.y))
        screen.blit(self.text_render, (self.x + (self.width - self.text_render.get_width()) // 2,
                                       self.y + (self.height - self.text_render.get_height()) // 2))

    def draw_image_button(self, screen, hover_image, idle_image, window_bg=colours.banner):
        self.check_image_button_state(hover_image, idle_image, screen,
                                      window_bg)  # Update button state based on mouse interaction
        screen.blit(self.surface, (self.x, self.y))

    def draw_mode_button(self, screen):
        self.check_mode_button_state(screen)

    def check_image_button_state(self, hover_icon, idle_icon, screen, window_bg):
        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()

        # Set button color based on hover and click state
        if self.is_hovered(mouse_pos):
            print("quit hovering")
            self.surface.fill(window_bg)
            self.surface.blit(hover_icon, (0, 0))
            if self.info_text:  # Check for info text and hover state
                self.show_info_text()
                text_rect = self.info_text.get_rect(topleft=(self.x + self.width + 5,
                                                             self.y + self.height // 2 - self.info_text.get_height() // 2))  # Adjust position
                screen.blit(self.info_text, text_rect)
                print("some info fo u")

        else:
            self.surface.fill(window_bg)
            self.surface.blit(idle_icon, (0, 0))
            self.hide_info_text()
            text_rect = self.info_text.get_rect(topleft=(self.x + self.width + 5,
                                                         self.y + self.height // 2 - self.info_text.get_height() // 2))  # Adjust position
            screen.blit(self.info_text, text_rect)

    def check_state(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()

        # Set button color based on hover and click state
        if self.is_hovered(mouse_pos):
            self.surface = create_rounded_rectangle(self.width, self.height, int(max(self.width, self.height) * 0.1),
                                                    self.hover_color)
            # if mouse_down[0]:  # Check if left mouse button is pressed
            #     self.surface = create_rounded_rectangle(self.width, self.height,
            #                                             int(max(self.width, self.height) * 0.1),
            #                                             self.click_color)
            #     self.click_func()  # Call the assigned function on click
        else:
            self.surface = create_rounded_rectangle(self.width, self.height, int(max(self.width, self.height) * 0.1),
                                                    self.idle_color)

    def decorate(self, screen):
        mines = self.generate_mine_count_surface()
        grid = self.generate_grid_size_surface()
        mine_offset = int(self.width * 0.2)  # Adjust offset as needed
        mine_x = self.x + mine_offset
        mine_y = self.y + self.surface.get_height() - 100

        # mine_icon, grid_icon = mines.copy(), grid.copy()
        mine_x, mine_y = self.x + 33, self.y + self.surface.get_height() - 60
        grid_x, grid_y = mines.get_width() // 2 + self.x + 83, self.y + self.surface.get_height() - 60
        screen.blit(self.mode_font,
                    (self.x + self.surface.get_width() // 2 - 13, self.y + self.surface.get_height() // 5))
        screen.blit(mines, (mine_x, mine_y))
        screen.blit(grid, (grid_x, grid_y))

    def generate_mine_count_surface(self: Mode):
        mine_count_image = pygame.Surface((icon_w, icon_h))
        mine_count_image.fill(ASH_GREY)

        mine = pygame.image.load(os.path.join(images_folder, "mine-detonated.png")).convert_alpha()
        mine = pygame.transform.scale(mine, (icon_h, icon_h))

        mine_count_image.blit(mine, (0, 0))
        count_image = LOGO_FONT.render(str(self.mode.mine_count), True, BLACK)
        mine_count_image.blit(count_image, (icon_h + 7, 0))
        return mine_count_image

    def generate_grid_size_surface(self: Mode):
        grid_size_info = pygame.Surface((icon_w, icon_h))
        grid_size_info.fill(ASH_GREY)

        grid_img = pygame.image.load(os.path.join(images_folder, "pixels.png")).convert_alpha()
        grid_img = pygame.transform.scale(grid_img, (icon_h, icon_h))

        grid_size_info.blit(grid_img, (0, 0))
        count_image = LOGO_FONT.render(str(self.mode.size) + " x " + str(self.mode.size), True, BLACK)
        grid_size_info.blit(count_image, (icon_h + 12, 0))
        return grid_size_info

    def check_mode_button_state(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()

        # Set button color based on hover and click state
        if self.is_hovered(mouse_pos):
            self.surface = create_rounded_rectangle(self.width, self.height, int(max(self.width, self.height) * 0.1),
                                                    self.hover_color)
            if mouse_down[0]:  # Check if left mouse button is pressed
                self.surface = create_rounded_rectangle(self.width, self.height,
                                                        int(max(self.width, self.height) * 0.1),
                                                        self.click_color)
                # self.click_func()  # Call the assigned function on click
        else:
            self.surface = create_rounded_rectangle(self.width, self.height, int(max(self.width, self.height) * 0.1),
                                                    self.idle_color)
        screen.blit(self.surface, (self.x, self.y))
        if hasattr(self, "mode"):
            self.decorate(screen)

    def is_hovered(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

    def is_clicked(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
