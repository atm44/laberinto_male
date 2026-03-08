import random
import pygame
import time
from load_global_variables import *
from motor_inteligencia_movimiento import RandomTraversal, TargetSeeker, TargetSeekerInMaze


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
        # Guardar posición anterior en caso de que se salga del laberinto
        pos_anterior = self.position.copy()
        
        # Calcular nuevo movimiento
        self.motor_inteligencia.aplicar_movimiento()
        self.position = self.motor_inteligencia.position
        
        # Validar que no se sale del laberinto
        maze = self.game.maze
        if maze:
            height = len(maze)
            width = len(maze[0]) if height > 0 else 0
            
            # Verificar que la posición redondeada está dentro de los límites
            x_redondeado = int(round(self.position[0]))
            y_redondeado = int(round(self.position[1]))
            
            # Si se sale del laberinto, restaurar posición anterior
            if x_redondeado < 0 or x_redondeado >= width or y_redondeado < 0 or y_redondeado >= height:
                self.position = pos_anterior
                self.motor_inteligencia.position = pos_anterior
        
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
    """Enemigo fantasma basico con motor de inteligencia aleatorio."""
    
    # Imagen definida en la clase
    image_path = "images/gastly.png"
    
    def __init__(self, game, x, y, image_path=None):
        # Usar la imagen de la clase si no se proporciona
        image_to_use = image_path if image_path else self.image_path
        
        # Crear un motor de movimiento aleatorio
        motor = random.choice([
            RandomTraversal(game, [x, y]),
            TargetSeeker(game, [x, y])
        ])
        # No llamar al super().__init__() de Ghost, sino al de Enemy con el motor
        Enemy.__init__(self, game, x, y, image_to_use, motor_inteligencia=motor)


class GhostMedium(Enemy):
    """Enemigo de nivel medio que persigue al jugador dentro del laberinto y puede teletransportarse."""
    
    # Imagen definida en la clase
    image_path = "images/hunter.png"
    
    def __init__(self, game, x, y, image_path=None):
        # Usar la imagen de la clase si no se proporciona
        image_to_use = image_path if image_path else self.image_path
        
        # Crear motor de movimiento que respeta paredes
        motor = TargetSeekerInMaze(game, [x, y])
        
        # Inicializar el enemigo base
        super().__init__(game, x, y, image_to_use, motor_inteligencia=motor)
        
        # Control de teletransportacion cada 10 segundos
        self.last_teleport_time = time.time()
        self.teleport_interval = 10  # segundos
        self.is_visible = True  # Para efecto visual de desaparicion
    
    def teletransportarse(self, player_position):
        """Teletransportarse a una posicion aleatoria en el laberinto."""
        maze = self.game.maze
        if not maze:
            return
        
        height = len(maze)
        width = len(maze[0]) if height > 0 else 0
        player_pos_grid = player_position.get_position_grid()
        
        # Generar nueva posicion aleatoria que no sea pared ni donde este el jugador
        while True:
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            
            if maze[y][x] != '#' and (y, x) != tuple(player_pos_grid):
                self.position = [x, y]
                self.motor_inteligencia.position = [x, y]
                # Recalcular el camino del motor
                self.motor_inteligencia._generar_objetivo()
                self.update()
                break
        
        self.last_teleport_time = time.time()
        self.is_visible = True
    
    def move(self, player_position=None):
        """Movimiento con posible teletransportacion cada 10 segundos."""
        current_time = time.time()
        
        # Verificar si es hora de teletransportarse
        if current_time - self.last_teleport_time >= self.teleport_interval and player_position:
            self.teletransportarse(player_position)
        
        # Llamar al movimiento normal del padre
        super().move()
