import pygame
import random

# Pygame başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 400, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Oyunu")

# Renkler
NUMBER_COLOR = {
    2: (255, 255, 0),
    4: (255, 165, 0),
    8: (255, 85, 0),
    16: (255, 165, 0),
    32: (255, 0, 0),
    64: (200, 0, 0),
    128: (255, 255, 0),
    256: (255, 200, 0),
    512: (255, 150, 0),
    1024: (255, 100, 0),
    2048: (255, 50, 0),
    4096: (255, 25, 0),
    8192: (200, 0, 200),
    16384: (150, 0, 150),
    32768: (100, 0, 100),
}

class GameManager:
    def __init__(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.spawn_number()
        self.spawn_number()

    def load_high_score(self):
        try:
            with open("game_2048/highscore.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("game_2048/highscore.txt", "w") as file:
                file.write(str(self.high_score))

    def spawn_number(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice([2, 4])

    def can_move(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return True
                if i < 3 and self.grid[i][j] == self.grid[i+1][j]:
                    return True
                if j < 3 and self.grid[i][j] == self.grid[i][j+1]:
                    return True
        return False

    def merge(self, row):
        new_row = [num for num in row if num != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
                self.score += new_row[i]
        new_row = [num for num in new_row if num != 0]
        return new_row + [0] * (4 - len(new_row))

    def move(self, direction):
        if self.game_over:
            return
        
        moved = False
        if direction == 'up':
            for j in range(4):
                col = [self.grid[i][j] for i in range(4)]
                new_col = self.merge(col)
                for i in range(4):
                    if self.grid[i][j] != new_col[i]:
                        moved = True
                    self.grid[i][j] = new_col[i]
        elif direction == 'down':
            for j in range(4):
                col = [self.grid[i][j] for i in range(4)][::-1]
                new_col = self.merge(col)[::-1]
                for i in range(4):
                    if self.grid[i][j] != new_col[i]:
                        moved = True
                    self.grid[i][j] = new_col[i]
        elif direction == 'left':
            for i in range(4):
                row = self.grid[i]
                new_row = self.merge(row)
                if self.grid[i] != new_row:
                    moved = True
                self.grid[i] = new_row
        elif direction == 'right':
            for i in range(4):
                row = self.grid[i][::-1]
                new_row = self.merge(row)[::-1]
                if self.grid[i] != new_row:
                    moved = True
                self.grid[i] = new_row
        
        if moved:
            self.spawn_number()
        
        if not self.can_move():
            self.game_over = True
            self.save_high_score()

    def draw(self):
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 64)
        score_font = pygame.font.Font(None, 32)
        game_over_font = pygame.font.Font(None, 48)
        
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                if value != 0:
                    color = NUMBER_COLOR.get(value, (200, 200, 200))
                    pygame.draw.rect(screen, color, (j * 100, i * 100, 100, 100))
                    text = font.render(str(value), True, (0, 0, 0))
                    screen.blit(text, (j * 100 + 35, i * 100 + 35))
        
        # Skor ve yüksek skor gösterme
        score_text = score_font.render(f"Skor: {self.score}", True, (0, 0, 0))
        high_score_text = score_font.render(f"Yüksek Skor: {self.high_score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 410))
        screen.blit(high_score_text, (200, 410))
        
        if self.game_over:
            game_over_text = game_over_font.render("Oyun Bitti!", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        
        pygame.display.flip()

# Oyun döngüsü
game = GameManager()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.move('up')
            elif event.key == pygame.K_DOWN:
                game.move('down')
            elif event.key == pygame.K_LEFT:
                game.move('left')
            elif event.key == pygame.K_RIGHT:
                game.move('right')
    game.draw()
pygame.quit()
