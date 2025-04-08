import random
from load_global_variables import *
from ui_helpers import *
class MazeGame:
    def __init__(self, width, height):
        self.cols = width if width % 2 == 1 else width + 1
        self.rows = height if height % 2 == 1 else height + 1
        self.maze = [['#'] * self.cols for _ in range(self.rows)]
        self.start = (1, 1)
        self.exit = (self.rows - 2, self.cols - 2)
        self.player = list(self.start)
        self.score = 0
        self.coins = set()
        self.generate_maze()
        self.spawn_coins(10)
        self.screen = None
        self.exit_img = None

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

    def draw(self, surface, player_name,width,height,selected_player):
        surface.fill(BLACK)
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (row, col) == tuple(self.player):
                    # pygame.draw.rect(surface, GREEN, rect)
                    pygame.draw.rect(surface, GRAY, rect)
                    self.screen.blit(selected_player, (col * CELL_SIZE,row * CELL_SIZE))
                elif (row, col) == self.exit:
                    pygame.draw.rect(surface, GRAY, rect)
                    self.screen.blit(self.exit_img, (col * CELL_SIZE,row * CELL_SIZE))
                elif (row, col) in self.coins:
                    pygame.draw.circle(surface, (255, 215, 0), rect.center, CELL_SIZE // 3)
                elif self.maze[row][col] == '#':
                    pygame.draw.rect(surface, WHITE, rect)
                else:
                    pygame.draw.rect(surface, GRAY, rect)

        # Dibujar nombre y puntuación
        score_text = f"{player_name}: {self.score}"
        score_text_size = 20
        draw_text(score_text,score_text_size,WHITE,(score_text_size*2,SCREEN_HEIGHT-score_text_size/2),self.screen) 
        

    def move_player(self, dx, dy):
        new_y = self.player[0] + dy
        new_x = self.player[1] + dx
        if self.maze[new_y][new_x] != '#':
            self.player = [new_y, new_x]
            if tuple(self.player) in self.coins:
                self.coins.remove(tuple(self.player))
                self.score += 100
