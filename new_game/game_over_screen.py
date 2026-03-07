import pygame
import sys
from load_global_variables import *
from ui_helpers import draw_text, draw_button


class GameOverScreen:
    """Pantalla de Game Over cuando el jugador pierde todas las vidas."""
    
    def __init__(self, game):
        self.game = game
        
        # Crear la imagen del corazón roto (pixel art estilo 90s)
        self.broken_heart_img = self.create_broken_heart_image()
        
        # Animación
        self.direction = 1
        self.scale = 1.0
        self.scale_speed = 0.03
    
    def create_broken_heart_image(self):
        """Crear imagen de corazón roto estilo pixel art (200x200)."""
        size = 200
        heart_img = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Colores
        RED = (200, 0, 0)
        DARK_RED = (100, 0, 0)
        
        # Dibujar corazón roto (dos mitades separadas con grietas)
        # Mitad izquierda (roja oscura)
        pygame.draw.polygon(heart_img, DARK_RED, [
            (50, 80),   # Top left
            (100, 50),  # Top middle
            (100, 110), # Middle
            (50, 140),  # Bottom left
            (30, 120),  # Left point
        ])
        
        # Mitad derecha (roja clara)
        pygame.draw.polygon(heart_img, RED, [
            (100, 110), # Middle
            (150, 140), # Bottom right
            (170, 120), # Right point
            (100, 50),  # Top middle
            (150, 80),  # Top right
        ])
        
        # Grieta en el medio
        pygame.draw.line(heart_img, (50, 0, 0), (100, 50), (100, 140), 3)
        
        # Pequeños píxeles rotos alrededor
        broken_pixels = [
            (95, 110), (105, 110), (98, 105), (102, 115),
            (90, 120), (110, 120), (85, 115), (115, 125)
        ]
        for px, py in broken_pixels:
            pygame.draw.rect(heart_img, DARK_RED, (px, py, 4, 4))
        
        return heart_img
    
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
        draw_text(f"Jugador: {self.game.name}", 24, WHITE, (SCREEN_WIDTH // 2, 360), screen)
        draw_text(f"Puntuación Final: {self.game.score}", 28, BLUE, (SCREEN_WIDTH // 2, 410), screen)
        
        # Botón volver al menú
        btn_menu = pygame.Rect(SCREEN_WIDTH // 2 - 100, 460, 200, 50)
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
