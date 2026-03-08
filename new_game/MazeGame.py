import random
from load_global_variables import *
from ui_helpers import *
from win_screen import WinScreen
from game_over_screen import GameOverScreen
from enemys import GhostBasic, GhostMedium
from player import Player
from coin import Coin

class MazeGame:
    def __init__(self, game):
        self.game = game
        
        # Establecer referencia a MazeGame en el objeto game (para acceso desde enemigos)
        self.game.maze_game = self

        self.window_width = game.width * CELL_SIZE  
        self.window_height = game.height * CELL_SIZE + 40  # espacio para el texto arriba
        
        self.cols = self.game.height if self.game.height % 2 == 1 else self.game.height + 1
        self.rows = self.game.width if self.game.width % 2 == 1 else self.game.width + 1
        self.maze = [['#'] * self.cols for _ in range(self.rows)]
        self.start = (1, 1)
        self.exit = (self.rows - 2, self.cols - 2)
        self.coins = []  # Lista de objetos Coin
        
        # Generar laberinto
        self.generate_maze()
        
        # Establecer el laberinto en el objeto game (para acceso desde enemigos)
        self.game.maze = self.maze
        
        self.spawn_coins(10)

        # Crear jugador
        self.player = Player(game, self.maze, self.start, game.selected_player)

        # Crear una lista para almacenar enemigos
        self.enemies = []
        self.spawn_enemies(5)  # Generar 5 enemigos como ejemplo    

    def game_loop(self):   
        self.draw()
        self.update_enemies()  # Actualizar enemigos
        self.check_coin_collection()  # Verificar monedas
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                # Pasar evento al jugador
                self.player.handle_input(event)
        
        # Procesar movimiento continuo
        self.player.process_movement()
        
        # Verificar si el jugador está vivo
        if not self.player.is_alive():
            self.game.current_screen = GameOverScreen(self.game)
            return
        
        # Verificar si llegó a la salida
        if tuple(self.player.get_position_grid()) == self.exit:
            self.game.current_screen = WinScreen(self.game)

    def spawn_enemies(self, amount):
        """Genera una cantidad especifica de enemigos en posiciones aleatorias."""
        player_pos = tuple(self.player.get_position_grid())
        for i in range(amount):
            while True:
                x = random.randint(1, self.cols - 2)
                y = random.randint(1, self.rows - 2)
                if self.maze[y][x] == ' ' and (y, x) != player_pos and (y, x) != self.exit:
                    # Crear una mezcla de GhostBasic y GhostMedium
                    # 60% GhostBasic, 40% GhostMedium
                    if random.random() < 0.6:
                        enemy = GhostBasic(self.game, x, y)
                    else:
                        enemy = GhostMedium(self.game, x, y)
                    self.enemies.append(enemy)
                    break

    def update_enemies(self):
        """Actualiza la posicion y renderiza a los enemigos."""
        for enemy in self.enemies:
            # Pasar al jugador si es un GhostMedium
            if isinstance(enemy, GhostMedium):
                enemy.move(self.player)
            else:
                enemy.move()
            
            enemy.check_collision_with_player(self.player)
            enemy.blit(self.game.screen)

    def generate_maze(self):
        def carve(x, y):
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.rows and 0 < ny < self.cols and self.maze[nx][ny] == '#':
                    self.maze[nx - dx // 2][ny - dy // 2] = ' '
                    self.maze[nx][ny] = ' '
                    carve(nx, ny)

        self.maze[self.start[0]][self.start[1]] = ' '
        carve(*self.start)
        self.maze[self.exit[0]][self.exit[1]] = 'E'

    def spawn_coins(self, amount):
        """Genera monedas en posiciones aleatorias del laberinto."""
        empty_spaces = [
            (r, c) for r in range(1, self.rows - 1)
            for c in range(1, self.cols - 1)
            if self.maze[r][c] == ' ' and (r, c) not in [self.start, self.exit]
        ]
        selected_positions = random.sample(empty_spaces, min(amount, len(empty_spaces)))
        self.coins = [Coin(c, r) for r, c in selected_positions]  # Crear objetos Coin

    def draw(self):
        self.game.screen.fill(BLACK)
        player_pos = tuple(self.player.get_position_grid())
        
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (row, col) == player_pos:
                    pygame.draw.rect(self.game.screen, GRAY, rect)
                    self.player.draw(self.game.screen)
                elif (row, col) == self.exit:
                    pygame.draw.rect(self.game.screen, GRAY, rect)
                    self.game.screen.blit(self.game.exit_img, (col * CELL_SIZE, row * CELL_SIZE))
                elif self.maze[row][col] == '#':
                    pygame.draw.rect(self.game.screen, WHITE, rect)
                else:
                    pygame.draw.rect(self.game.screen, GRAY, rect)

        # Dibujar monedas
        for coin in self.coins:
            coin.draw(self.game.screen)
        
        # Dibujar nombre y puntuación
        score_text = f"{self.game.name}: {self.game.score}"
        score_text_size = 20
        draw_text(score_text, score_text_size, WHITE, (score_text_size, self.window_height - score_text_size), self.game.screen, aligment="midleft")
        
        # Dibujar vidas (corazones) en la esquina inferior derecha
        self.draw_lives()

    def check_coin_collection(self):
        """Verificar si el jugador recolectó monedas."""
        coins_recogidas = []
        for coin in self.coins:
            if coin.check_collision_with_rect(self.player.rect):
                coins_recogidas.append(coin)
                # Asegurar que el puntaje no sea negativo
                self.game.score = max(0, self.game.score + 100)
        
        # Remover las monedas recogidas
        for coin in coins_recogidas:
            self.coins.remove(coin)
    
    def draw_lives(self):
        """Dibujar vidas (corazones) en la esquina inferior derecha."""
        lives = self.player.get_lives()
        heart_size = 30
        spacing = 5
        
        # Posición inicial (esquina inferior derecha)
        start_x = self.window_width - (heart_size + spacing) * 3 - 10
        start_y = self.window_height - heart_size - 10
        
        # Dibujar tantos corazones como vidas tenga
        for i in range(lives):
            x = start_x + i * (heart_size + spacing)
            y = start_y
            # Dibujar corazón escalado
            heart_img = pygame.transform.scale(self.game.victory_img, (heart_size, heart_size))
            self.game.screen.blit(heart_img, (x, y))
