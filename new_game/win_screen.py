from load_global_variables import *
from ui_helpers import *

class WinScreen:
    def __init__(self, game):
        self.game = game

        # Animación: variables
        self.direction = 1
        self.scale = 1
        self.scale_speed = 0.02

    def render(self):
        # Redimensionar pantalla al tamaño original
        if self.game.screen.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
            self.game.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        victory_img = self.game.victory_img
        screen = self.game.screen

        # Dibujar pantalla de victoria
        screen.fill(BLACK)
        draw_text(" ESCAPASTE! GENIAA! ", 36, GREEN, (320, 60), screen)

        # Animar la imagen (agrandar y achicar)
        min_scale = 0.5
        max_scale = 3
        scaled_size = int(0.25 * SCREEN_WIDTH * self.scale)
        img = pygame.transform.smoothscale(victory_img, (scaled_size, scaled_size))
        img_rect = img.get_rect(center=(320, 200))
        # print(self.scale)
        # print(self.direction)
        screen.blit(img, img_rect)

        # Botón volver
        btn_back = pygame.Rect(220, 360, 200, 50)
        draw_button(btn_back, "Volver al Menu", screen)

        pygame.display.flip()

        # Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos):
                    self.game.current_screen = self.game.start_screen

        # Lógica de animación
        self.scale += self.scale_speed * self.direction
        if self.scale >= max_scale:
            self.scale = max_scale
            self.direction *= -1
        elif self.scale <= min_scale:
            self.scale = min_scale    
            self.direction *= -1