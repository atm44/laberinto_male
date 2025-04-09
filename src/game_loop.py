from load_global_variables import *
from MazeGame import *
from win_screen import *
import asyncio

def game_loop(width, height, player_name,selected_player,exit_img,victory_img,clock):
    global screen
    window_width = width * CELL_SIZE
    window_height = height * CELL_SIZE + 40  # espacio para el texto arriba
    screen = pygame.display.set_mode((window_width, window_height))

    game = MazeGame(width, height)
    game.screen = screen
    game.exit_img = exit_img
    win = False
    while not win:
        game.draw(screen, player_name,0,window_height - 40,selected_player)
        pygame.display.flip()
        await asyncio.sleep(0)  # Give control back to the main thread
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    game.move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    game.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_player(1, 0)

        if tuple(game.player) == game.exit:
            win = True
    win_screen(clock,victory_img)
