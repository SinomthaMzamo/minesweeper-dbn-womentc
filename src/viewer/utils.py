import os
import pygame

pygame.init()

project_dir = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]  # Get root directory
images_folder = os.path.join(project_dir, "assets/images")
fonts_folder = os.path.join(project_dir, "assets/fonts")

def generate_home_button_image(image_path: str):
    size = 150 // 2
    home_image = pygame.image.load(os.path.join(images_folder, image_path)).convert_alpha()
    home_image = pygame.transform.scale(home_image, (size, size))
    return home_image