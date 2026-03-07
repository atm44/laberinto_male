import os
import pygame


from load_global_variables import *
from start_screen import StartScreen    



# ------------ pygame mode setup ------------
class Game():
    def __init__(self,snd_folder,img_folder) -> None:
        self.snd_folder = snd_folder
        self.img_folder = img_folder
        self.clock = pygame.time.Clock()
        


        # ----- initialize pygame
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Laberinto de Male")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        music_backgroud_path = os.path.join(self.snd_folder,"music_background_1.ogg")
        print(f"{music_backgroud_path=}")
        pygame.mixer.music.load(music_backgroud_path)
        pygame.mixer.music.play(-1)
        
        self.victory_img = pygame.image.load(os.path.join(self.img_folder,"corazon.png")).convert_alpha()
        self.logo_img = pygame.image.load(os.path.join(self.img_folder,"cara_male_editada.png")).convert_alpha()
        exit_img = pygame.image.load(os.path.join(self.img_folder,"pokeball.png")).convert_alpha()
        self.basic_ghost_img_path = os.path.join(self.img_folder,"gastly.png")       
        self.exit_img = pygame.transform.scale(exit_img, (CELL_SIZE, CELL_SIZE))

        self.width = 15
        self.height = 15
        self.name = ""
        self.score = 0
        self.start_screen = StartScreen(self)
        self.current_screen = self.start_screen 
        self.selected_player = None


    def run(self) -> None:
        """
        Running the game in local Pygame mode with a synchronous main loop.
        """
        running = True
        while running:
            try:
                self.current_screen.render()
                self.clock.tick(60)  # Control FPS global a 60 FPS
            except SystemExit:
                running = False
                break



