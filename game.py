#locals:
from game_loop import *
from win_screen import *
from select_character_screen import *
from start_screen import *
from load_global_variables import *

# from MazeGame import *



pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("./sonidos/Peaceful Oasis (cdef6aa6cf2f4941a19c48303fa7c8e8).mp3")
pygame.mixer.music.play(-1)
font = pygame.font.SysFont(FONT_NAME, 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Laberinto!")
clock = pygame.time.Clock()

victory_img = pygame.image.load("./imagenes/corazon.png").convert_alpha()
logo_img = pygame.image.load("./imagenes/cara_male_editada.png").convert_alpha()
exit_img = pygame.image.load("./imagenes/pokeball.png").convert_alpha()


exit_img = pygame.transform.scale(exit_img, (CELL_SIZE, CELL_SIZE))

def main():
    while True:
        width, height, player_name = start_screen(clock,logo_img)
        selected_player = select_character_screen(clock)
        game_loop(width, height, player_name,selected_player,exit_img,victory_img,clock)


if __name__ == "__main__":
    main()