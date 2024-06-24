from random import choice

import pygame
import colours
import fonts
import sys
from game_build.minesweeper import Board, Game
from game_build.tile import SafeTile




# TODO:
# 1. SETUP THE GRID
# > create a window
WIDTH = 540
HEIGHT = 540

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

colour_map = {
    0: colours.ASH_GREY,
    1: colours.PINK,
    2: colours.TURQUOISE,
    3: colours.LILAC,
    4: colours.LIGHT_ORANGE,
    5: colours.TOMATO,
    6: colours.DEEP_SKY_BLUE,
    7: colours.PALE_YELLOW,
    8: colours.CELADON_GREEN
}



def draw_board(board: Board):
    rows = board.get_rows()
    columns = board.get_columns()
    size = WIDTH//columns

    numbers_font = pygame.font.Font(fonts.ROBOTO, size-5)
    number_images = []
    for mine_count in range(1, 9):
        number_img = numbers_font.render(str(mine_count), True, colours.BLACK)
        number_images.append(number_img)

    unrevealed_tile_img = pygame.Surface((size, size))
    unrevealed_tile_img.fill(colours.ASH_GREY)

    # load flag image
    flag = pygame.image.load("flag.png").convert_alpha()
    flag = pygame.transform.scale(flag, (size-5, size-5))

    flagged_tile_img = pygame.Surface((size, size))
    

    revealed_tile_blank_img = pygame.Surface((size, size))
    revealed_tile_blank_img.fill(colours.CARAMEL)

    bomb = pygame.image.load("simple_bomb.png").convert_alpha()
    bomb = pygame.transform.scale(bomb, (size-10,size-10))
    revealed_mine_tile_img = pygame.Surface((size, size))
    


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
                        # find image centre
                        flag_x = size*x // 2 - (size*x - 5) // 2
                        flag_y = size*y // 2 - (size*y - 5) // 2
                        flagged_tile_img.fill(colours.ASH_GREY)
                        flagged_tile_img.blit(flag, (flag_x,flag_y))
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
                            screen.blit(number_images[mine_count - 1], (x, y))
                        else:
                            # don't show number and don't change colour
                            revealed_tile_blank_img.fill(colours.BEIGE)
                            screen.blit(revealed_tile_blank_img, (x, y))
                    else:
                        # find image centre
                        bomb_x = size*x // 2 - (size*x - 10) // 2
                        bomb_y = size*y // 2 - (size*y - 5) // 2
                        # update revealed mine tile with image
                        revealed_mine_tile_img.fill(colours.SALMON)
                        revealed_mine_tile_img.blit(bomb, (bomb_x, bomb_y))
                        screen.blit(revealed_mine_tile_img, (x, y))
    pygame.display.flip()

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

def main():
    game_modes = ["easy", "medium", "hard"]
    mode = choice(game_modes)

    # create Board instance
    board1 = Board("easy")

    # create Game instance 
    minesweeper = Game(board1)
    # create mainloop

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                selected_tile = get_grid_location_of_tile(mouse_position, minesweeper.get_game_board())
                tile = minesweeper.get_game_board().get_tile_from_locale(selected_tile)
                if isinstance(tile, tuple):
                    minesweeper.board.set_up_game_board(selected_tile)
                    continue
                flag = event.button == 3
                print(event.button, flag)
                minesweeper.run_game(selected_tile, flag)
                print("mouse click!", selected_tile)
                if flag: print("flag toggled")
        draw_window(board1)
    close()



if __name__ == "__main__":
    main()