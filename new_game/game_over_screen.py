import pygame
import sys
from load_global_variables import *
from ui_helpers import draw_text, draw_button


class GameOverScreen:
    """Pantalla de Game Over cuando el jugador pierde todas las vidas."""
    
    def __init__(self, game):
        self.game = game
        
        # Cargar la imagen del corazón roto
        self.broken_heart_img = pygame.image.load("images/corazon_roto.png")
        
        # Animación
        self.direction = 1
        self.scale = 1.0
        self.scale_speed = 0.03
    
    
    def render(self):
        """Renderizar pantalla de Game Over."""
        # Redimensionar pantalla si es necesario
        if self.game.screen.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
            self.game.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        screen = self.game.screen
        screen.fill(BLACK)
        
        # Dibujar título
        draw_text("GAME OVER", 48, RED, (SCREEN_WIDTH // 2, 60), screen)
        
        # Animar corazón roto (agrandar y achicar)
        min_scale = 0.8
        max_scale = 1.3
        self.scale += self.scale_speed * self.direction
        if self.scale >= max_scale or self.scale <= min_scale:
            self.direction *= -1
        
        scaled_size = int(200 * self.scale)
        scaled_heart = pygame.transform.scale(self.broken_heart_img, (scaled_size, scaled_size))
        heart_rect = scaled_heart.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(scaled_heart, heart_rect)
        
        # Dibujar información del jugador
        draw_text(f"Jugador: {self.game.name}", 24, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT-200), screen)
        draw_text(f"Puntuación Final: {self.game.score}", 28, BLUE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT-40), screen)
        
        # Botón volver al menú
        btn_menu = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT-120, 200, 50)
        draw_button(btn_menu, "Volver al Menú", screen)
        
        pygame.display.flip()
        
        # Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_menu.collidepoint(event.pos):
                    # Resetear puntuación y volver al menú
                    self.game.score = 0
                    self.game.current_screen = self.game.start_screen
