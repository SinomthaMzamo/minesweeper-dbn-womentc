import pygame

# Initialize Pygame
pygame.init()

# Screen size
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# Rectangle parameters
rect_x = 50
rect_y = 50
rect_width = 100
rect_height = 60
roundness = 9  # Adjust for desired corner roundness

# Create a surface for the rectangle outer layer
rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
rect_surface.fill((0, 0, 0, 0))  # Transparent background

# Draw the rounded rectangle with border_radius, has same dimensions as surface
pygame.draw.rect(rect_surface, red, (0, 0, rect_width, rect_height), border_radius=roundness)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill((255, 255, 255))

    # Blit the rounded rectangle onto the screen
    screen.blit(rect_surface, (rect_x, rect_y))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()


def create_rounded_rectangle(width, height, radius, colour):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    pygame.draw.rect(surface, colour, (0, 0, width, height), border_radius=radius)
    return surface
