import random
from load_global_variables import *
from ui_helpers import *
from win_screen import WinScreen
class MazeGame:
    def __init__(self,game):
        self.game = game

        self.window_width = game.width * CELL_SIZE  
        self.window_height = game.height * CELL_SIZE + 40 # espacio para el texto arriba
        
        self.cols = self.game.height if self.game.height % 2 == 1 else self.game.height + 1
        self.rows = self.game.width if self.game.width % 2 == 1 else self.game.width + 1
        self.maze = [['#'] * self.cols for _ in range(self.rows)]
        self.start = (1, 1)
        self.exit = (self.rows - 2, self.cols - 2)
        self.player = list(self.start)
        self.score = 0
        self.coins = set()
        self.generate_maze()
        self.spawn_coins(10)

        
        

    def game_loop(self):   


        self.draw()
        pygame.display.flip()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_player(1, 0)

        if tuple(self.player) == self.exit:
            self.game.current_screen = WinScreen(self.game)


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
        empty_spaces = [
            (r, c) for r in range(1, self.rows - 1)
            for c in range(1, self.cols - 1)
            if self.maze[r][c] == ' ' and (r, c) not in [self.start, self.exit]
        ]
        self.coins = set(random.sample(empty_spaces, min(amount, len(empty_spaces))))

    def draw(self):
        self.game.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.game.screen.fill(BLACK)
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (row, col) == tuple(self.player):
                    pygame.draw.rect(self.game.screen, GRAY, rect)
                    self.game.screen.blit(self.game.selected_player, (col * CELL_SIZE,row * CELL_SIZE))
                elif (row, col) == self.exit:

                    pygame.draw.rect(self.game.screen, GRAY, rect)
                    self.game.screen.blit(self.game.exit_img, (col * CELL_SIZE,row * CELL_SIZE))
                elif (row, col) in self.coins:
                    pygame.draw.circle(self.game.screen, (255, 215, 0), rect.center, CELL_SIZE // 3)
                elif self.maze[row][col] == '#':
                    pygame.draw.rect(self.game.screen, WHITE, rect)
                else:
                    pygame.draw.rect(self.game.screen, GRAY, rect)

        # Dibujar nombre y puntuación
        score_text = f"{self.game.name}: {self.score}"
        score_text_size = 20
        draw_text(score_text,score_text_size,WHITE,(score_text_size,SCREEN_HEIGHT-score_text_size),self.game.screen,aligment="left") 
        pygame.display.flip()

    def move_player(self, dx, dy):
        
        new_y = self.player[0] + dy
        new_x = self.player[1] + dx

        # print(f'Moving player to ({new_x}, {new_y})')
        # print(f'maze type:{self.maze[new_y][new_x]}')
        if self.maze[new_y][new_x] != '#':
            self.player = [new_y, new_x]
            if tuple(self.player) in self.coins:
                self.coins.remove(tuple(self.player))
                self.score += 100
