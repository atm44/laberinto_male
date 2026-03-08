import pygame
from load_global_variables import *


class Player:
    """Clase que encapsula toda la lógica del jugador."""
    
    def __init__(self, game, maze, start_pos, image):
        """
        Inicializa el jugador.
        
        Args:
            game: Referencia al objeto Game
            maze: Referencia al laberinto (para colisiones)
            start_pos: Tupla (y, x) - posición inicial en grid
            image: Imagen del jugador pygame.Surface
        """
        self.game = game
        self.maze = maze
        
        # Posición en GRID
        self.position = list(start_pos)  # [y, x]
        
        # Imagen
        self.image = image
        
        # Rect en PÍXELES (para renderizado y colisiones)
        self.rect = self.image.get_rect()
        self.update_rect()
        
        # Movimiento
        self.speed = 1
        self.orientation = "right"  # "right" o "left"
        
        # Sistema de vidas
        self.lives = 3
        self.last_collision_time = 0  # Evitar colisiones múltiples rápidas
        
        # Input
        self.keys_pressed = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
        }
    
    def update_rect(self):
        """Sincronizar rect (píxeles) con position (grid)"""
        pixel_x = self.position[1] * CELL_SIZE  # column * CELL_SIZE
        pixel_y = self.position[0] * CELL_SIZE  # row * CELL_SIZE
        self.rect.topleft = (pixel_x, pixel_y)
    
    def handle_input(self, event):
        """Procesar eventos de teclado."""
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = True
        
        elif event.type == pygame.KEYUP:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = False
                self.process_movement()
    
    def process_movement(self):
        """Procesar movimiento según teclas presionadas."""
        if self.keys_pressed[pygame.K_UP]:
            self.move(0, -self.speed)
        elif self.keys_pressed[pygame.K_DOWN]:
            self.move(0, self.speed)
        elif self.keys_pressed[pygame.K_LEFT]:
            self.move(-self.speed, 0)
            self.orientation = "left"
        elif self.keys_pressed[pygame.K_RIGHT]:
            self.move(self.speed, 0)
            self.orientation = "right"
    
    def move(self, dx, dy):
        """
        Mover el jugador en el grid.
        
        Args:
            dx: Cambio en x (columna)
            dy: Cambio en y (fila)
        """
        new_y = self.position[0] + dy
        new_x = self.position[1] + dx
        
        # Verificar que no choques con paredes
        if self.maze[new_y][new_x] != '#':
            self.position = [new_y, new_x]
            self.update_rect()
    
    def collect_coin(self, coin_pos):
        """Recoger una moneda."""
        if tuple(self.position) == coin_pos:
            self.game.score = max(0, self.game.score + 100)  # Asegurar que no sea negativo
            return True
        return False
    
    def check_collision_with_enemy(self, enemy_rect):
        """
        Verificar colisión con un enemigo.
        
        Args:
            enemy_rect: pygame.Rect del enemigo
            
        Returns:
            True si hay colisión, False en caso contrario
        """
        return self.rect.colliderect(enemy_rect)
    
    def draw(self, screen):
        """Dibujar el jugador en la pantalla."""
        if self.orientation == "left":
            screen.blit(self.image, self.rect)
        elif self.orientation == "right":
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
    
    def get_position_grid(self):
        """Obtener posición en grid [y, x]."""
        return self.position
    
    def get_position_pixel(self):
        """Obtener posición en píxeles (x, y)."""
        return (self.rect.x, self.rect.y)
    
    def lose_life(self):
        """Perder una vida (con cooldown para evitar múltiples colisiones rápidas)."""
        import time
        current_time = time.time()
        # Cooldown de 1 segundo entre colisiones
        if current_time - self.last_collision_time > 1.0:
            self.lives = max(0, self.lives - 1)
            self.last_collision_time = current_time
            return True
        return False
    
    def is_alive(self):
        """Verificar si el jugador sigue vivo."""
        return self.lives > 0
    
    def get_lives(self):
        """Obtener número de vidas."""
        return self.lives
