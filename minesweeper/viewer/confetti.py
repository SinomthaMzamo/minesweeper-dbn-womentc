import  pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("confetti")

COLORS = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (0, 255, 255),   # Cyan
    (255, 0, 255),   # Magenta
    (255, 165, 0),   # Orange
    (128, 0, 128),   # Purple
    (255, 192, 203),  # Pink
    (255, 182, 193), # Pastel Red
    (119, 221, 119), # Pastel Green
    (173, 216, 230), # Pastel Blue
    (253, 253, 150), # Pastel Yellow
    (186, 255, 255), # Pastel Cyan
    (255, 187, 255), # Pastel Magenta
    (255, 209, 220), # Pastel Orange
    (219, 112, 147), # Pastel Purple
    (255, 228, 225), # Pastel Pink
    (192, 192, 192), # Silver
    (255, 215, 0),   # Gold
    (205, 127, 50),  # Bronze
    (184, 115, 51)   # Copper
]


class Confetti:
    def __init__(self, x,y):
        self.x, self.y = x, y
        self.height = random.randint(5,12)
        self.colour = random.choice(COLORS)
        self.speed_x = random.uniform(-2,2)
        self.speed_y = random.uniform(1,3)
        self.gravity = 0.011              # increments the vertical speed

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity

    def draw(self, screen_parm):
        pygame.draw.rect(screen_parm, self.colour, (self.x, self.y, 3, self.height))
        print("there should be colour!!")


def create_confetti(num_particles):
    confetti_particles = []
    for _ in range(num_particles):
        x = random.randint(0, 800)
        y = random.randint(0, 12)
        confetti_particles.append(Confetti(x, y))
    return confetti_particles



if __name__ == "__main__":

    # Main loop
    running = True
    confetti_particles = []
    player_won = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Simulate player win condition
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_won = True
                confetti_particles = create_confetti(700)

        # Fill the screen with a color
        screen.fill((255, 255, 255))

        if player_won:
            for confetti in confetti_particles:
                confetti.update()  # Update position based on speed and gravity
                confetti.draw(screen)  # Draw confetti at updated position



        win_image_paths = ["win-purple.png", "win-green.png", "win-pink.png"]
        win_image_path =  random.choice(win_image_paths)
        win_image = pygame.image.load(win_image_path).convert_alpha()
        win_image = pygame.transform.scale(win_image,(120, 120))
        screen.blit(win_image,(800//2, 600//3))
        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()