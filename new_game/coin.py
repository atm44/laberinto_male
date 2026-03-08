import pygame
from load_global_variables import *


class Coin:
    """Clase que representa una moneda en el laberinto."""
    
    def __init__(self, x, y):
        """
        Inicializa una moneda.
        
        Args:
            x: Posición X en grid
            y: Posición Y en grid
        """
        # Cargar y escalar la imagen
        self.image = pygame.image.load("images/coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        
        # Posición en GRID
        self.position = (x, y)
        
        # Rect en PÍXELES
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
    
    def draw(self, screen):
        """Dibuja la moneda en la pantalla."""
        screen.blit(self.image, self.rect)
    
    def get_position(self):
        """Obtiene la posición en grid."""
        return self.position
    
    def check_collision_with_rect(self, rect):
        """
        Verifica si la moneda colisiona con un rect (del jugador).
        
        Args:
            rect: pygame.Rect del jugador
            
        Returns:
            True si hay colisión, False en caso contrario
        """
        return self.rect.colliderect(rect)
