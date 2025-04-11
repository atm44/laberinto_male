# Third-party imports
import asyncio
from copy import deepcopy
import math
import os
from random import choice, randint
from typing import Any
import pygame
# from pygame_emojis import load_emoji
import sys

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
        music_backgroud_path = os.path.join(self.snd_folder,"music_background_1.ogg")
        print(f"{music_backgroud_path=}")
        pygame.mixer.music.load(music_backgroud_path)
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.victory_img = pygame.image.load(os.path.join(self.img_folder,"corazon.png")).convert_alpha()
        self.logo_img = pygame.image.load(os.path.join(self.img_folder,"cara_male_editada.png")).convert_alpha()
        exit_img = pygame.image.load(os.path.join(self.img_folder,"pokeball.png")).convert_alpha()

        self.exit_img = pygame.transform.scale(exit_img, (CELL_SIZE, CELL_SIZE))

        self.width = 15
        self.height = 15
        self.name = ""
        self.start_screen = StartScreen(self)
        self.current_screen = self.start_screen 
        self.selected_player = None


    async def run(self) -> None:
        """
        Running the game in Pygame mode means continuous cycles.
        The logic is different and a bit more complicated.
        """


        while True:
            # ----- checking for any event like key presses
            # self.check_events()
            # self.main_game_loop(10, 10)
            self.current_screen.render()
            await asyncio.sleep(0)



