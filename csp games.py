import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
RED = (255, 99, 71)
GREEN = (50, 205, 50)
PURPLE = (147, 112, 219)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

class GamePortal:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("AI CSP Games Portal")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.current_game = "portal"
        
        # Game states
        self.n_queens_n = 8
        self.n_queens_board = [-1] * self.n_queens_n
        
        self.sudoku_grid = np.array([
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ])
        
        self.map_regions = {
            'A': [(100, 100), (200, 50), (300, 100), (250, 200)],
            'B': [(300, 100), (400, 50), (500, 100), (450, 200), (350, 250)],
            'C': [(100, 200), (250, 200), (350, 250), (150, 300)],
            'D': [(350, 250), (450, 200), (550, 250), (450, 350), (300, 300)]
        }
        self.map_colors = {'A': None, 'B': None, 'C': None, 'D': None}
        
    def draw_gradient_background(self):
        for y in range(700):
            color = (
                int(79 + (6 - 79) * y / 700),
                int(70 + (182 - 70) * y / 700), 
                int(229 + (212 - 229) * y / 700)
            )
            pygame.draw.line(self.screen, color, (0, y), (1000, y))
    
    def draw_portal(self):
        self.draw_gradient_background()
        
        # Title
        title = self.title_font.render("🎮 AI CSP Games Portal", True, WHITE)
        subtitle = self.font.render("Fun meets Artificial Intelligence – Explore, Play & Learn!", True, WHITE)
        self.screen.blit(title, (500 - title.get_width()//2, 80))
        self.screen.blit(subtitle, (500 - subtitle.get_width()//2, 150))
        
        # Game cards
        cards = [
            ("🧩 Sudoku Solver", "Input numbers and let AI solve automatically!", 250),
            ("👑 N-Queens Solver", "Solve the classic N-Queens problem!", 400),
            ("🗺️ Map Coloring", "Color regions with no adjacent same colors!", 550)
        ]
        
        for title, desc, y_pos in cards:
            self.draw_game_card(title, desc, y_pos)
    
    def draw_game_card(self, title, description, y_pos):
        card_rect = pygame.Rect(200, y_pos, 600, 120)
        
        # Card background with blur effect
        s = pygame.Surface((600, 120), pygame.SRCALPHA)
        s.fill((255, 255, 255, 50))
        self.screen.blit(s, (200, y_pos))
        
        pygame.draw.rect(self.screen, (255, 255, 255, 100), card_rect, border_radius=20)
        pygame.draw.rect(self.screen, WHITE, card_rect, 2, border_radius=20)
        
        # Text
        title_text = self.font.render(title, True, WHITE)
        desc_text = self.font.render(description, True, (224, 231, 255))
        self.screen.blit(title_text, (300, y_pos + 30))
        self.screen.blit(desc_text, (300, y_pos + 70))
        
        # Button
        btn_rect = pygame.Rect(650, y_pos + 40, 100, 40)
        pygame.draw.rect(self.screen, BLUE, btn_rect, border_radius=20)
        btn_text = self.font.render("Play", True, WHITE)
        self.screen.blit(btn_text, (675, y_pos + 45))
    
    def draw_n_queens(self):
        self.draw_gradient_background()
        
        # Title
        title = self.title_font.render("♛ N-Queens Solver ♛", True, WHITE)
        self.screen.blit(title, (500 - title.get_width()//2, 30))
        
        # Board
        board_size = 400
        cell_size = board_size // self.n_queens_n
        start_x = (1000 - board_size) // 2
        start_y = 150
        
        # Draw chess board
        for i in range(self.n_queens_n):
            for j in range(self.n_queens_n):
                color = WHITE if (i + j) % 2 == 0 else GRAY
                rect = pygame.Rect(start_x + j * cell_size, start_y + i * cell_size, cell_size, cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                
                # Draw queen
                if self.n_queens_board[i] == j:
                    queen_text = self.font.render("♛", True, (250, 204, 21))
                    self.screen.blit(queen_text, (start_x + j * cell_size + cell_size//3, 
                                                start_y + i * cell_size + cell_size//4))
        
        # Buttons
        buttons = [("Reset", 300, 600), ("Hint", 450, 600), ("AI Solve", 600, 600)]
        for text, x, y in buttons:
            btn_rect = pygame.Rect(x, y, 100, 40)
            pygame.draw.rect(self.screen, BLUE, btn_rect, border_radius=20)
            btn_text = self.font.render(text, True, WHITE)
            self.screen.blit(btn_text, (x + 50 - btn_text.get_width()//2, y + 10))
    
    def draw_sudoku(self):
        self.draw_gradient_background()
        
        # Title
        title = self.title_font.render("🧩 Sudoku Solver", True, WHITE)
        self.screen.blit(title, (500 - title.get_width()//2, 30))
        
        # Sudoku board
        board_size = 450
        cell_size = board_size // 9
        start_x = (1000 - board_size) // 2
        start_y = 120
        
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, WHITE, (start_x, start_y + i * cell_size), 
                           (start_x + board_size, start_y + i * cell_size), line_width)
            pygame.draw.line(self.screen, WHITE, (start_x + i * cell_size, start_y), 
                           (start_x + i * cell_size, start_y + board_size), line_width)
        
        # Numbers
        for i in range(9):
            for j in range(9):
                if self.sudoku_grid[i][j] != 0:
                    num_text = self.font.render(str(self.sudoku_grid[i][j]), True, WHITE)
                    self.screen.blit(num_text, (start_x + j * cell_size + cell_size//3,
                                              start_y + i * cell_size + cell_size//4))
        
        # Buttons
        buttons = [("Hint", 350, 600), ("Check", 500, 600), ("Reset", 650, 600)]
        for text, x, y in buttons:
            btn_rect = pygame.Rect(x, y, 100, 40)
            pygame.draw.rect(self.screen, BLUE, btn_rect, border_radius=20)
            btn_text = self.font.render(text, True, WHITE)
            self.screen.blit(btn_text, (x + 50 - btn_text.get_width()//2, y + 10))
    
    def draw_map_coloring(self):
        self.draw_gradient_background()
        
        # Title
        title = self.title_font.render("🗺️ Map Coloring", True, WHITE)
        self.screen.blit(title, (500 - title.get_width()//2, 30))
        
        # Color palette
        palette_y = 100
        for i, color in enumerate(COLORS[:5]):
            pygame.draw.rect(self.screen, color, (100 + i * 70, palette_y, 50, 50))
        
        # Draw regions
        for region, points in self.map_regions.items():
            color = self.map_colors[region] if self.map_colors[region] else WHITE
            pygame.draw.polygon(self.screen, color, points)
            pygame.draw.polygon(self.screen, BLACK, points, 2)
            
            # Region label
            center_x = sum(p[0] for p in points) // len(points)
            center_y = sum(p[1] for p in points) // len(points)
            label = self.font.render(region, True, BLACK)
            self.screen.blit(label, (center_x - 10, center_y - 10))
        
        # Buttons
        buttons = [("Solve", 400, 600), ("Reset", 550, 600)]
        for text, x, y in buttons:
            btn_rect = pygame.Rect(x, y, 100, 40)
            pygame.draw.rect(self.screen, BLUE, btn_rect, border_radius=20)
            btn_text = self.font.render(text, True, WHITE)
            self.screen.blit(btn_text, (x + 50 - btn_text.get_width()//2, y + 10))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.current_game == "portal":
                    # Check portal buttons
                    if 650 < mouse_pos[0] < 750 and 290 < mouse_pos[1] < 330:
                        self.current_game = "sudoku"
                    elif 650 < mouse_pos[0] < 750 and 440 < mouse_pos[1] < 480:
                        self.current_game = "nqueens"
                    elif 650 < mouse_pos[0] < 750 and 590 < mouse_pos[1] < 630:
                        self.current_game = "mapcoloring"
                
                elif self.current_game == "nqueens":
                    # Back button
                    if 50 < mouse_pos[0] < 150 and 50 < mouse_pos[1] < 90:
                        self.current_game = "portal"
                
                elif self.current_game == "mapcoloring":
                    # Back button
                    if 50 < mouse_pos[0] < 150 and 50 < mouse_pos[1] < 90:
                        self.current_game = "portal"
    
    def run(self):
        while True:
            self.handle_events()
            
            if self.current_game == "portal":
                self.draw_portal()
            elif self.current_game == "nqueens":
                self.draw_n_queens()
            elif self.current_game == "sudoku":
                self.draw_sudoku()
            elif self.current_game == "mapcoloring":
                self.draw_map_coloring()
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    portal = GamePortal()
    portal.run()