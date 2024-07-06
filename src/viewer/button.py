import pygame


class Button:
    def __init__(self, x, y, width, height, text, font, idle_color, hover_color, click_color, click_func):
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
        self.surface = pygame.Surface((width, height))
        self.text_render = font.render(text, True, (0, 0, 0))  # Pre-render text for efficiency

    def draw(self, screen):
        self.check_state()  # Update button state based on mouse interaction
        screen.blit(self.surface, (self.x, self.y))
        screen.blit(self.text_render, (self.x + (self.width - self.text_render.get_width()) // 2,
                                       self.y + (self.height - self.text_render.get_height()) // 2))

    def check_state(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()

        # Set button color based on hover and click state
        if self.is_hovered(mouse_pos):
            self.surface.fill(self.hover_color)
            if mouse_down[0]:  # Check if left mouse button is pressed
                self.surface.fill(self.click_color)
                self.click_func()  # Call the assigned function on click
        else:
            self.surface.fill(self.idle_color)

    def is_hovered(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

    def is_clicked(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height