from random import choice

import pygame
import colours
import fonts
import sys
from game_build.minesweeper import Board
from game_build.tile import SafeTile, MineTile


# TODO:
# 1. SETUP THE GRID
# > create a window
WIDTH = 900
HEIGHT = 900




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
numbers_font = pygame.font.Font(fonts.GROTESQUE, 32)
number_images = []
for mine_count in range(1,9):
    number_img = numbers_font.render(str(mine_count), True, colours.BLACK)
    number_images.append(number_img)

colour_map = {
    0: colours.ASH_GREY,
    1: colours.SKY_BLUE,
    2: colours.MINT_GREEN,
    3: colours.PALE_YELLOW,
    4: colours.PEACH,
    5: colours.TOMATO,
    6: colours.PASTEL_LAVENDER,
    7: colours.DARK_ORANGE,
    8: colours.SEAFOAM_GREEN
}



def draw_board(board: Board):
    rows = board.get_rows()
    columns = board.get_columns()
    size = WIDTH//columns

    unrevealed_tile_img = pygame.Surface((size, size))
    unrevealed_tile_img.fill(colours.DEEP_SKY_BLUE)

    # load flag image
    flag = pygame.image.load("../../assets/images/flag.png")
    flag = pygame.transform.scale(flag, (size-5, size-5))

    flagged_tile_img = pygame.Surface((size-5, size-5))
    flagged_tile_img.fill(colours.ASH_GREY)
    flagged_tile_img.blit(flag, (0,0))

    revealed_tile_blank_img = pygame.Surface((size, size))
    revealed_tile_blank_img.fill(colours.CARAMEL)

    revealed_mine_tile_img = pygame.Surface((size, size))
    bomb = pygame.image.load("../../assets/simple_bomb.png")
    bomb = pygame.transform.scale(bomb, (size,size))
    revealed_mine_tile_img.blit(bomb, (size-5, size-5))

    for row in range(rows):
        for col in range(columns):
            tile = board.get_tile_from_locale((row, col))
            x = col*size
            y = row*size
            pygame.draw.rect(screen, colours.BLACK,
                             (x - 2, y - 2, size + 2 * 2, size + 2 * 2), 2)
            # draw tile on grid using it's top left corner coordinate
            if isinstance(tile, tuple):
                screen.blit(unrevealed_tile_img, (x, y))
            else:
                if not tile.is_revealed:
                    if tile.is_flagged:
                        screen.blit(flagged_tile_img, (x, y))
                    else:
                        screen.blit(unrevealed_tile_img, (x, y))
                else:
                    if isinstance(tile, SafeTile):
                        # count number of mines in neighbourhood
                        mine_count = tile.count_neighbourhood_mines()
                        if mine_count > 0:
                            # show the number
                            revealed_tile_blank_img.fill(colour_map[mine_count])
                            screen.blit(revealed_tile_blank_img, (x, y))
                            screen.blit(number_images[mine_count - 1], (x + 5, y + 5))
                        else:
                            # don't show number and don't change colour
                            screen.blit(revealed_tile_blank_img, (x, y))
                    else:
                        screen.blit(revealed_mine_tile_img, (x, y))
    pygame.display.flip()

# #
# public boolean isIn(Position topLeft, Position bottomRight) {
#         boolean withinTop = this.y <= topLeft.getY();
#         boolean withinBottom = this.y >= bottomRight.getY();
#         boolean withinLeft = this.x >= topLeft.getX();
#         boolean withinRight = this.x <= bottomRight.getX();
#         return withinTop && withinBottom && withinLeft && withinRight;
#     }

def get_grid_location_of_tile(mouse_click_location: tuple, board: Board):
    tile_location_x = mouse_click_location[0] // board.get_tile_size(WIDTH)
    tile_location_y = mouse_click_location[1] // board.get_tile_size(WIDTH)
    if (0 <= tile_location_x < board.get_columns()
            and 0 <= tile_location_y < board.get_rows()):
        return tile_location_y, tile_location_x






def draw_window(board):
    screen.fill(colours.SILVER)
    draw_board(board)
    pygame.display.update()

def close():
    """
    closes the game window
    """
    pygame.quit()
    sys.exit()

def main(board: Board):
    # create mainloop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                selected_tile = get_grid_location_of_tile(mouse_position, board)
                print("mouse click!", selected_tile)
        draw_window(board)
    close()

# 2. EACH TILE ON THE GRID IS A BUTTON AT FIRST
# 3. OKAY


if __name__ == "__main__":
    # get game mode
    game_modes = ["easy", "medium", "hard"]
    mode = choice(game_modes)

    main(Board("easy"))