from load_global_variables import *
from ui_helpers import *
import os
from game_loop import GameLoop

class SelectCharacterScreen:
    def __init__(self, game):
        self.game = game
        self.selected_image = None
        # Load and scale player images
        self.characters_selection = []
        self.characters_players = []
        for i in range(1, 4):
            img_path = os.path.join(self.game.img_folder, f"player_{i}.png")
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (CELL_SIZE*5, CELL_SIZE*5))
            img_player = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
            self.characters_selection.append(img)
            self.characters_players.append(img_player)

        # Set positions
        self.positions = [
            (160, 200),
            (320, 200),
            (480, 200)
        ]

    def render(self):    
        self.game.screen.fill(BLACK)
        draw_text("Elegí tu personaje", 36, WHITE, (320, 80),self.game.screen)

        # Draw images
        for i, img in enumerate(self.characters_selection):
            rect = img.get_rect(center=self.positions[i])
            self.game.screen.blit(img, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, pos in enumerate(self.positions):
                    rect = self.characters_selection[i].get_rect(center=pos)
                    if rect.collidepoint(event.pos):
                        self.game.selected_player = self.characters_players[i]
                        self.game.current_screen = GameLoop(self.game)                        
        
        # clock.tick(60)

