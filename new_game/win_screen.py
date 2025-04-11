from load_global_variables import *
from ui_helpers import *

class WinScreen:
    def __init__(self, game):
        self.game = game

        # Animación: variables
        self.direction = 1
        self.scale = 1.0
        self.scale_speed = 0.2
        self.screen = self.game.screen

        

    def render(self):
        self.game.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        victory_img = self.game.victory_img
        



        # Dibujar pantalla de victoria
        self.screen.fill(BLACK)
        draw_text(" ESCAPASTE! GENIAA! ", 36, GREEN, (320, 60),self.screen)

        # Animar la imagen (agrandar y achicar)
        min_scale = 0.5
        max_scale = 1.5
        scaled_size = int(0.25 * SCREEN_WIDTH * self.scale)
        img = pygame.transform.smoothscale(victory_img, (scaled_size, scaled_size))
        img_rect = img.get_rect(center=(320, 200))
        self.screen.blit(img, img_rect)

        # Botón volver
        btn_back = pygame.Rect(220, 360, 200, 50)
        draw_button(btn_back, "Volver al Menu",self.screen)

        pygame.display.flip()

        # Lógica de animación
        self.scale += self.scale_speed * self.direction
        if self.scale >= max_scale or self.scale <= min_scale:
            self.scale_speed *= -1
        self.direction *= -1
        # print(f'{self.scale=}')
        # print(f'{self.direction=}')
        # print(f'{self.scale_speed=}')
        # print(f'{scaled_size=}')
        self.game.clock.tick(10)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos):
                    self.game.current_screen = self.game.start_screen
        

