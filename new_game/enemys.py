import random
import pygame
from load_global_variables import *

class Enemy:
    def __init__(self, game, x, y, image_path):
        self.game = game
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image , (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        # Guardar posición en GRID (para lógica de juego)
        self.position = [x, y]
        # Rect SIEMPRE en píxeles (para dibujo y colisiones)
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
        self.speed = 0.1  # Velocidad del enemigo (movimiento suave)
        self.direction = (0, 0)  # Dirección inicial

    def move(self):
        """Método base para movimiento, puede ser sobrescrito por subclases."""
        pass

    def check_collision_with_player(self):
        """Verifica si el enemigo colisiona con el jugador."""
        player = self.game.selected_player
        if self.rect.colliderect(player.get_rect()):
            self.game.score -= 100  # El jugador pierde 100 puntos

    def blit(self, screen):
        """Dibuja la imagen del enemigo en la pantalla."""
        # Rect ya está en píxeles, usar directamente
        screen.blit(self.image, self.rect)
    
    def update(self):
        """Sincronizar rect (píxeles) con position (grid)"""
        x = round(self.position[0]) * CELL_SIZE
        y = round(self.position[1]) * CELL_SIZE
        self.rect.topleft = x, y

class Ghost(Enemy):
    def __init__(self, game, x, y, image_path):
        super().__init__(game, x, y, image_path)

    def move(self):
        """Movimiento suave aleatorio que puede atravesar paredes."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Derecha, Abajo, Izquierda, Arriba
        self.direction = random.choice(directions)
        self.position[0] = (self.position[0] + self.direction[0] * self.speed)
        self.position[1] = (self.position[1] + self.direction[1] * self.speed)
        # Sincronizar rect con la nueva posición
        self.update()

class GhostBasic(Ghost):
    def __init__(self, game, x, y, image_path):
        super().__init__(game, x, y, image_path)

    def move(self):
        """Movimiento suave básico."""
        super().move()  # Usa el movimiento aleatorio de Ghost
        self.check_collision_with_player()