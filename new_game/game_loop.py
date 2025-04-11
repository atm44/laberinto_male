from load_global_variables import *
from MazeGame import *

class GameLoop:
    def __init__(self, global_game):
        self.name = ""
        self.active = False
        self.input_box = pygame.Rect(20, 120, 200, 36)
        self.game = MazeGame(global_game)
    
    def render(self):
        self.game.game_loop()

