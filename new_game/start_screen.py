
from load_global_variables import *
from ui_helpers import draw_text, draw_button
from select_character_screen import SelectCharacterScreen

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.name = ""
        self.active = False
        self.input_box = pygame.Rect(20, 120, 200, 36)

    def render(self):
        self.game.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        select_character_screen = SelectCharacterScreen(self.game)
        # Llenar la pantalla con color blanco
        self.game.screen.fill(WHITE)

        # Dibujar textos
        draw_text("Laberinto de male", 48, BLACK, (320, 60), self.game.screen)
        draw_text("Nombre:", 24, BLACK, (65, 100), self.game.screen)

        # Dibujar cuadro de entrada
        pygame.draw.rect(self.game.screen, BLACK, self.input_box, 2)

        # Dibujar imagen
        img = pygame.transform.smoothscale(self.game.logo_img, (400, 400))
        img_rect = img.get_rect(center=(420, 300))
        self.game.screen.blit(img, img_rect)

        # Mostrar el nombre
        if self.game.name == "":
            name_to_show = "Escribe aquí..."
        else:
            name_to_show = self.game.name
        if self.active:
            name_to_show = self.name
        draw_text(name_to_show, 24, BLACK, self.input_box.center, self.game.screen)

        # Dibujar botones
        btn_small = pygame.Rect(20, 180, 200, 40)
        btn_medium = pygame.Rect(20, 230, 200, 40)
        btn_large = pygame.Rect(20, 280, 200, 40)
        btn_exit = pygame.Rect(20, 340, 200, 40)

        draw_button(btn_small, "Pequeño (15x15)", self.game.screen)
        draw_button(btn_medium, "Mediano (21x21)", self.game.screen)
        draw_button(btn_large, "Grande (31x31)", self.game.screen)
        draw_button(btn_exit, "Salir", self.game.screen)

        pygame.display.flip()

        for event in pygame.event.get():

            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.input_box.collidepoint(event.pos):
                    self.active = True  

                    pygame.draw.rect(self.game.screen, WHITE, self.input_box, 2)
                else:

                    self.active = False
                if btn_small.collidepoint(event.pos) and self.name:
                    self.game.width = 15
                    self.game.height = 15
                    self.game.name = self.name
                    self.game.current_screen = select_character_screen
                    
                
                elif btn_medium.collidepoint(event.pos) and self.name:
                    self.game.width = 21
                    self.game.height = 21
                    self.game.name = self.name
                    self.game.current_screen = select_character_screen

                elif btn_large.collidepoint(event.pos) and self.name:
                    self.game.width = 31
                    self.game.height = 31
                    self.game.name = self.name
                    self.game.current_screen = select_character_screen


                elif btn_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    if len(self.name) < 12:
                        self.name += event.unicode

        # self.game.clock.tick(30)