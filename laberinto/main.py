import asyncio
from laberinto.assets.game_loop import *
from laberinto.assets.win_screen import *
from laberinto.assets.select_character_screen import *
from laberinto.assets.start_screen import *
from laberinto.assets.load_global_variables import *

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("./laberinto/sonidos/music_background_1.ogg")
pygame.mixer.music.play(-1)
font = pygame.font.SysFont(FONT_NAME, 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Laberinto!")
clock = pygame.time.Clock()

victory_img = pygame.image.load("./laberinto/imagenes/corazon.png").convert_alpha()
logo_img = pygame.image.load("./laberinto/imagenes/cara_male_editada.png").convert_alpha()
exit_img = pygame.image.load("./laberinto/imagenes/pokeball.png").convert_alpha()
exit_img = pygame.transform.scale(exit_img, (CELL_SIZE, CELL_SIZE))

async def main():
    while True:
        width, height, player_name = start_screen(clock, logo_img)
        selected_player = select_character_screen(clock)
        game_loop(width, height, player_name, selected_player, exit_img, victory_img, clock)
        await asyncio.sleep(0)  # Give control back to the main thread

if __name__ == "__main__":
    asyncio.run(main())
