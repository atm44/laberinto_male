import random
import pygame
from load_global_variables import *

class Enemy:
    def __init__(self, game, x, y, image_path):
        self.game = game
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image , (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = [x, y]
        self.speed = 0.1  # Velocidad del enemigo (movimiento suave)
        self.direction = (0, 0)  # Dirección inicial

    def move(self):
        """Método base para movimiento, puede ser sobrescrito por subclases."""
        pass

    def check_collision_with_player(self):
        """Verifica si el enemigo colisiona con el jugador."""
        player = self.game.selected_player
        print(f"Enemy rect: {self.rect}, Player rect: {player.get_rect()}")
        if self.rect.colliderect(player.get_rect()):
            self.game.score -= 100  # El jugador pierde 100 puntos

    def blit(self, screen):
        """Dibuja la imagen del enemigo en la pantalla."""
        screen.blit(self.image, (self.rect.x * CELL_SIZE, 
                                 self.rect.y * CELL_SIZE))
    def update(self):
        x = round(self.position[0])
        y = round(self.position[1])
        self.rect.topleft = x, y

class Ghost(Enemy):
    def __init__(self, game, x, y, image_path):
        super().__init__(game, x, y, image_path)

    def move(self):
        """Movimiento suave aleatorio que puede atravesar paredes."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Derecha, Abajo, Izquierda, Arriba
        self.direction = random.choice(directions)
        print(f'Enemy position: {self.rect.x}, {self.rect.y}')
        print(f'Moving in direction: {self.direction}')
        self.position[0] = (self.position[0] + self.direction[0] * self.speed) #% self.game.current_screen.cols
        self.position[1] = (self.position[1] + self.direction[1] * self.speed) #% self.game.current_screen.rows
        print(f'Enemy position: {self.rect.x}, {self.rect.y}')

class GhostBasic(Ghost):
    def __init__(self, game, x, y, image_path):
        super().__init__(game, x, y, image_path)

    def move(self):
        """Movimiento suave básico."""
        super().move()  # Usa el movimiento aleatorio de Ghost
        self.check_collision_with_player()