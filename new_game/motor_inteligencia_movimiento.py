import random
import math


class MotorInteligenciaMovimiento:
    """Clase base para los motores de movimiento de enemigos."""
    
    def __init__(self, game, position):
        """
        Inicializa el motor de movimiento.
        
        Args:
            game: Referencia al objeto Game
            position: Posición inicial [x, y]
        """
        self.game = game
        self.position = position
        self.speed = 0.1  # Velocidad del movimiento
        self.direction = (0, 0)
    
    def calcular_movimiento(self):
        """
        Calcula la dirección del movimiento. Debe ser sobrescrito por subclases.
        
        Returns:
            Tupla (dx, dy) con el cambio de posición
        """
        raise NotImplementedError("Las subclases deben implementar calcular_movimiento()")
    
    def aplicar_movimiento(self):
        """Aplica el movimiento calculado a la posición."""
        dx, dy = self.calcular_movimiento()
        self.position[0] += dx * self.speed
        self.position[1] += dy * self.speed


class RandomTraversal(MotorInteligenciaMovimiento):
    """Motor que genera movimiento aleatorio que atraviesa paredes."""
    
    def __init__(self, game, position):
        super().__init__(game, position)
        self.direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
    
    def calcular_movimiento(self):
        """Devuelve un movimiento aleatorio cada vez."""
        # Cambiar dirección aleatoriamente (con cierta probabilidad)
        if random.random() < 0.1:  # 10% de probabilidad de cambiar dirección
            self.direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        
        return self.direction


class TargetSeeker(MotorInteligenciaMovimiento):
    """Motor que se mueve hacia un objetivo aleatorio en el mapa."""
    
    def __init__(self, game, position):
        super().__init__(game, position)
        self.maze = game.maze if hasattr(game, 'maze') else None
        self.target = None
        self.distancia_llegada = 0.5  # Distancia para considerar que llegó al objetivo
        self._generar_objetivo()
    
    def _generar_objetivo(self):
        """Genera un nuevo objetivo aleatorio en el mapa."""
        if not self.maze:
            self.target = None
            return
        
        # Elegir un punto aleatorio que no sea pared
        height = len(self.maze)
        width = len(self.maze[0]) if height > 0 else 0
        
        while True:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            # Asegurarse de que no es una pared
            if self.maze[y][x] != '#':
                self.target = [x, y]
                break
    
    def calcular_movimiento(self):
        """Calcula el movimiento hacia el objetivo."""
        if not self.target:
            print("No hay objetivo establecido, generando uno nuevo.")
            self._generar_objetivo()
            return (0, 0)
        
        # Verificar si llegó al objetivo
        distancia = math.sqrt(
            (self.position[0] - self.target[0]) ** 2 + 
            (self.position[1] - self.target[1]) ** 2
        )
        
        if distancia < self.distancia_llegada:
            print(f"Enemigo llegó al objetivo {self.target}, generando nuevo objetivo.")
            self._generar_objetivo()
            return (0, 0)
        
        # Calcular la dirección hacia el objetivo
        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        
        # Normalizar la dirección
        magnitud = math.sqrt(dx ** 2 + dy ** 2)
        if magnitud > 0:
            dx /= magnitud
            dy /= magnitud
        
        # Elegir la dirección más cercana a la dirección calculada
        # (de las 4 direcciones posibles)
        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        mejor_direccion = max(
            direcciones,
            key=lambda d: dx * d[0] + dy * d[1]  # Producto punto
        )
        
        return mejor_direccion
