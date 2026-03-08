import random
import pygame
from load_global_variables import *
from motor_inteligencia_movimiento import RandomTraversal, TargetSeeker


class Enemy:
    """Clase base para enemigos."""
    
    def __init__(self, game, x, y, image_path, motor_inteligencia=None):
        """
        Inicializa un enemigo.
        
        Args:
            game: Referencia al objeto Game
            x: Posición X en grid
            y: Posición Y en grid
            image_path: Ruta de la imagen del enemigo
            motor_inteligencia: Motor de movimiento (MotorInteligenciaMovimiento)
        """
        self.game = game
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        
        # Guardar posición en GRID (para lógica de juego)
        self.position = [x, y]
        # Rect SIEMPRE en píxeles (para dibujo y colisiones)
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
        
        self.speed = 0.1  # Velocidad del enemigo (movimiento suave)
        self.direction = (0, 0)  # Dirección inicial
        
        # Motor de inteligencia de movimiento
        self.motor_inteligencia = motor_inteligencia if motor_inteligencia else RandomTraversal(game, self.position)

    def move(self):
        """Método base para movimiento, delega al motor de inteligencia."""
        # print(f"Enemigo en {self.position} calculando movimiento con motor {self.motor_inteligencia.__class__.__name__}")
        self.motor_inteligencia.aplicar_movimiento()
        self.position = self.motor_inteligencia.position
        self.update()

    def check_collision_with_player(self, player):
        """
        Verifica si el enemigo colisiona con el jugador.
        
        Args:
            player: Objeto Player
        """
        if self.rect.colliderect(player.rect):
            self.game.score -= 100  # El jugador pierde 100 puntos
            player.lose_life()  # Perder una vida

    def blit(self, screen):
        """Dibuja la imagen del enemigo en la pantalla."""
        screen.blit(self.image, self.rect)

    def update(self):
        """Sincronizar rect (píxeles) con position (grid)"""
        x = round(self.position[0]) * CELL_SIZE
        y = round(self.position[1]) * CELL_SIZE
        self.rect.topleft = x, y


class Ghost(Enemy):
    """Enemigo fantasma con movimiento aleatorio."""
    
    def __init__(self, game, x, y, image_path):
        super().__init__(game, x, y, image_path)

    def move(self):
        """Movimiento suave aleatorio que puede atravesar paredes."""
        super().move()  # El movimiento se maneja en la clase base con el motor de inteligencia


class GhostBasic(Ghost):
    """Enemigo fantasma básico con motor de inteligencia aleatorio."""
    
    def __init__(self, game, x, y, image_path):
        # Crear un motor de movimiento aleatorio
        motor = random.choice([
            RandomTraversal(game, [x, y]),
            TargetSeeker(game, [x, y])
        ])
        # print(f"Creando GhostBasic en ({x}, {y}) con motor {motor.__class__.__name__}")
        # No llamar al super().__init__() de Ghost, sino al de Enemy con el motor
        Enemy.__init__(self, game, x, y, image_path, motor_inteligencia=motor)