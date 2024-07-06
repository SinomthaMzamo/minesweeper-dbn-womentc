import pygame
from random import choice
from game_build.minesweeper import Board, Game
from game_build.tile import SafeTile
import sys
import fonts
from constants import *
import time
# drawing functionalities related to the game board,
# like draw_board, draw_window, and updating flag/time displays, to this class.
# These functions will take the game board object and other necessary data as arguments.

class BoardPen:
    def __init__(self, game:Game, screen):
        self.screen = screen
        self.game = game
        self.rows = game.get_game_board().get_rows()
        self.columns = game.get_game_board().get_columns()
        self.tile_size = min(GRID_WIDTH // self.columns, GRID_HEIGHT // self.rows)           # Adjust size to fit grid area

    def generate_number_images(self, ):
        # Prepare number images for tiles
        numbers_font = pygame.font.Font(fonts.GEOLOGICA, self.tile_size - 5)
        number_images = [numbers_font.render(str(mine_count), True, colours.BLACK) for mine_count in range(1, 9)]
        return number_images

    def generate_unrevealed_tile_image(self, colour_path:str=colours.ASH_GREY):
        # Create surfaces for unrevealed tiles
        unrevealed_tile_img = pygame.Surface((self.tile_size, self.tile_size))
        unrevealed_tile_img.fill(colour_path)
        return unrevealed_tile_img

    def generate_flagged_tile_image(self, image_path:str, colour_path:str=colours.ASH_GREY):
        size = self.tile_size
        flag_icon = pygame.image.load(image_path).convert_alpha()
        flag_icon = pygame.transform.scale(flag_icon, (size - 5, size - 5))
        flagged_tile_img = pygame.Surface((size, size))
        flagged_tile_img.fill(colour_path)
        return flagged_tile_img, flag_icon

    def generate_blank_revealed_tile(self, colour_path:str=colours.BEIGE):
        revealed_tile_blank_img = pygame.Surface((self.tile_size, self.tile_size))
        revealed_tile_blank_img.fill(colour_path)
        return revealed_tile_blank_img

    def generate_revealed_bomb_image(self, image_path:str, colour_path=colours.TOMATO):
        size = self.tile_size
        bomb = pygame.image.load(image_path).convert_alpha()
        bomb = pygame.transform.scale(bomb, (size - 5, size - 5))
        revealed_mine_tile_img = pygame.Surface((size, size))
        revealed_mine_tile_img.fill(colour_path)
        return revealed_mine_tile_img, bomb

    def draw_window(self, game: Game, elapsed_time: int):
        """
        Draws the main window with the Minesweeper board centered within the designated grid area.

        Args:
        - board: The Minesweeper board object to draw.
        """
        self.screen.fill(colours.SNOW)
        self.update_flags(game)
        self.track_time(game, elapsed_time)
        self.draw()
        pygame.display.update()


    def draw(self):
        size = self.tile_size
        number_images = self.generate_number_images()
        unrevealed_tile_img = self.generate_unrevealed_tile_image()
        flagged_tile_img, flag = self.generate_flagged_tile_image("../../assets/images/grey.png")
        revealed_tile_blank_img = self.generate_blank_revealed_tile()
        revealed_mine_tile_img, bomb = self.generate_revealed_bomb_image("../../assets/spikes.png")

        # Iterate through each tile in the board and draw it within the grid area
        for row in range(self.rows):
            for col in range(self.columns):
                tile = self.game.get_game_board().get_tile_from_locale((row, col))
                x = GRID_TOP_LEFT_X + col * size
                y = GRID_TOP_LEFT_Y + row * size
                pygame.draw.rect(self.screen, colours.SLATE_GREY, (x - 2, y - 2, size + 2 * 2, size + 2 * 2), 2)

                # Determine how to draw the tile based on its type and state
                if isinstance(tile, tuple):
                    self.screen.blit(unrevealed_tile_img, (x, y))
                else:
                    if not tile.is_revealed:
                        if tile.is_flagged:
                            flag_x = size * x // 2 - (size * x - 5) // 2
                            flag_y = size * y // 2 - (size * y - 5) // 2
                            flagged_tile_img.blit(flag, (flag_x, flag_y))
                            self.screen.blit(flagged_tile_img, (x, y))
                        else:
                            self.screen.blit(unrevealed_tile_img, (x, y))
                    else:
                        if isinstance(tile, SafeTile):
                            mine_count = tile.count_neighbourhood_mines()
                            if mine_count > 0:
                                revealed_tile_blank_img.fill(colour_map[mine_count])
                                self.screen.blit(revealed_tile_blank_img, (x, y))
                                self.screen.blit(number_images[mine_count - 1], (x, y))
                            else:
                                revealed_tile_blank_img.fill(colours.BEIGE)
                                self.screen.blit(revealed_tile_blank_img, (x, y))
                        else:
                            # find image centre
                            bomb_x = size * x // 2 - (size * x - 10) // 2
                            bomb_y = size * y // 2 - (size * y - 5) // 2
                            # update revealed mine tile with image
                            revealed_mine_tile_img.blit(bomb, (bomb_x, bomb_y))
                            self.screen.blit(revealed_mine_tile_img, (x, y))
        pygame.display.flip()

    def update_flags(self, game: Game):
        flag = pygame.image.load("../../assets/images/grey.png").convert_alpha()
        flag = pygame.transform.scale(flag, (32, 32))

        flags_font = pygame.font.Font(fonts.GEOLOGICA, 20)
        flags_placed_img = flags_font.render(str(game.get_number_of_flags_placed()) + "/" + str(game.get_mine_count()),
                                             True, colours.BLACK)
        flag_progress = pygame.Surface((50, 50))
        flag_progress.fill(colours.LIGHT_GREY)
        self.screen.blit(flag, (GRID_TOP_LEFT_X - 50 * 2 + 15, 50))
        self.screen.blit(flags_placed_img, (GRID_TOP_LEFT_X - 50 * 2, GRID_TOP_LEFT_X - 65))

    def track_time(self, game: Game, elapsed_time: int):
        clock = pygame.image.load("../../assets/images/clock.png").convert_alpha()
        clock = pygame.transform.scale(clock, (50, 50))
        self.screen.blit(clock, (GRID_TOP_LEFT_X - 50 * 2 + 5, 150))

        timer_font = pygame.font.Font(fonts.GEOLOGICA, 20)
        timer_img = timer_font.render(f"{elapsed_time // 60:02}:{elapsed_time % 60:02}", True, colours.BLACK)
        self.screen.blit(timer_img, (GRID_TOP_LEFT_X - 50 * 3 + 60, 200))