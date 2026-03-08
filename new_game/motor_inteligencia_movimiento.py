import random
import math
from collections import deque


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
        

class TargetSeekerInMaze(MotorInteligenciaMovimiento):
    """Motor que se mueve hacia un objetivo usando pathfinding dentro del laberinto."""
    
    def __init__(self, game, position):
        super().__init__(game, position)
        self.maze = game.maze if hasattr(game, 'maze') else None
        self.target = None
        self.path = []  # Camino calculado mediante BFS
        self.path_index = 0
        self._generar_objetivo()
    
    def _generar_objetivo(self):
        """Genera un nuevo objetivo aleatorio en el mapa (no en paredes)."""
        if not self.maze:
            self.target = None
            return
        
        height = len(self.maze)
        width = len(self.maze[0]) if height > 0 else 0
        
        while True:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            if self.maze[y][x] != '#':
                self.target = [x, y]
                self.path = []
                self.path_index = 0
                break
    
    def _calcular_camino_bfs(self):
        """Calcula el camino mas corto hacia el objetivo usando BFS."""
        if not self.target or not self.maze:
            return []
        
        start = (int(round(self.position[0])), int(round(self.position[1])))
        goal = (self.target[0], self.target[1])
        
        if start == goal:
            return []
        
        queue = deque([(start, [start])])
        visited = {start}
        height = len(self.maze)
        width = len(self.maze[0]) if height > 0 else 0
        
        while queue:
            (x, y), path = queue.popleft()
            
            # Vecinos: arriba, derecha, abajo, izquierda
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    if self.maze[ny][nx] != '#':
                        new_path = path + [(nx, ny)]
                        
                        if (nx, ny) == goal:
                            return new_path[1:]  # Excluir el inicio
                        
                        visited.add((nx, ny))
                        queue.append(((nx, ny), new_path))
        
        return []  # No hay camino
    
    def calcular_movimiento(self):
        """Calcula el movimiento hacia el objetivo respetando paredes."""
        if not self.target:
            self._generar_objetivo()
            return (0, 0)
        
        # Verificar si llego al objetivo
        distancia = math.sqrt(
            (self.position[0] - self.target[0]) ** 2 + 
            (self.position[1] - self.target[1]) ** 2
        )
        
        if distancia < 0.5:
            self._generar_objetivo()
            return (0, 0)
        
        # Recalcular camino si esta vacio
        if not self.path:
            self.path = self._calcular_camino_bfs()
            self.path_index = 0
        
        # Si aun no hay camino, moverse hacia el objetivo de forma directa
        if not self.path:
            dx = self.target[0] - self.position[0]
            dy = self.target[1] - self.position[1]
            magnitud = math.sqrt(dx ** 2 + dy ** 2)
            if magnitud > 0:
                dx /= magnitud
                dy /= magnitud
            
            direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            return max(direcciones, key=lambda d: dx * d[0] + dy * d[1])
        
        # Seguir el camino
        if self.path_index < len(self.path):
            next_pos = self.path[self.path_index]
            current_pos = (int(round(self.position[0])), int(round(self.position[1])))
            
            # Si llegamos al siguiente punto del camino, avanzar
            if current_pos == next_pos:
                self.path_index += 1
                if self.path_index >= len(self.path):
                    self.path = []
                    return (0, 0)
                next_pos = self.path[self.path_index]
            
            # Calcular direccion hacia el siguiente punto del camino
            dx = next_pos[0] - current_pos[0]
            dy = next_pos[1] - current_pos[1]
            
            return (dx, dy)
        
        return (0, 0)
