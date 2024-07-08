import pygame
import os
from src.viewer.constants import *
from src.viewer import fonts
from src.viewer.button import Button
from src.viewer.utils import generate_home_button_image
from src.viewer.landing import main as launch

project_dir = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]  # Get root directory
images_folder = os.path.join(project_dir, "assets/images")
fonts_folder = os.path.join(project_dir, "assets/fonts")
clips_folder = os.path.join(project_dir, "assets/clips")
sprites_folder = os.path.join(project_dir, "assets/sprite-sheets")

pygame.init()



lose_spritesheet = pygame.image.load(os.path.join(sprites_folder, "clipped-lose-sheet.png"))
dupe_sheet = pygame.image.load(os.path.join(sprites_folder, "clipped-lose-sheet.png"))
number_of_frames = 20

frame_width = lose_spritesheet.get_width() // number_of_frames
frame_height = lose_spritesheet.get_height()


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


def crop_frame(self):
    pass
    cropped_image_width = self.frame_width - 100  # desired width
    cropped_image_height = self.frame_height - 100  # desired height
    cropped_image_surface = pygame.Surface((cropped_image_width, cropped_image_height))
    # Define the cropping area (x, y, width, height)
    x_to_crop = 0  # x-coordinate of the top-left corner of unwanted area
    y_to_crop = 0  # y-coordinate of the top-left corner of unwanted area
    crop_width = 8  # width of the unwanted area
    crop_height = 8  # height of the unwanted area
    crop_rect = (x_to_crop, y_to_crop, crop_width, crop_height)
    pygame.draw.rect(self.get_current_frame(), (0, 0, 0), (x_to_crop, y_to_crop, crop_width, crop_height), 20)

def draw_home_button(screen, home_button):
    idle_home_icon = generate_home_button_image("home(1).png")
    hovered_home_icon = generate_home_button_image("home(2).png")
    home_button.draw_image_button(screen, hovered_home_icon, idle_home_icon)


def draw_preview_window():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SCALED, vsync=2)
    screen.fill(colours.CELADON_GREEN)
    pygame.display.set_caption("game play preview")
    clock = pygame.time.Clock()

    # Create animation instance
    animation = Animation(lose_spritesheet, frame_width, frame_height)

    home_button = Button(90, WINDOW_HEIGHT - 100, 100, 100, ".",
                         pygame.font.Font(os.path.join(fonts_folder, fonts.ROBOTO), 30),
                         colours.THISTLE, colours.THISTLE, colours.CELADON_GREEN, launch,
                         "Returns to main page")

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # pos = pygame.mouse.get_pos()
                # if home_button.is_clicked(pos):
                #     return main()

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

def run():
    draw_preview_window()


if __name__ == "__main__":
    draw_preview_window()
