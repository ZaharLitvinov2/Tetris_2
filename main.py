import pygame
import sys
import random
from pygame.locals import *
from board import Board
from tetromino import Tetromino

# Инициализация pygame
pygame.init()

# Настройки игры
CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SIDEBAR_WIDTH = 200
SCREEN_WIDTH = BOARD_WIDTH * CELL_SIZE + SIDEBAR_WIDTH + 40
SCREEN_HEIGHT = BOARD_HEIGHT * CELL_SIZE + 40
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GHOST_COLOR = (100, 100, 100)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Тетрис')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)

class Game:
    def __init__(self):
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        self.game_board = self.board.create()
        self.current_piece = Tetromino.get_random_tetromino()
        self.next_piece = Tetromino.get_random_tetromino()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.fall_speed = self.calculate_fall_speed()  # Начальная скорость падения
        self.last_fall = pygame.time.get_ticks()
        self.paused = False

    def calculate_fall_speed(self):
        """Вычисляет скорость падения на основе текущего уровня"""
        # Базовое время между падениями (в мс)
        base_speed = 1000
        # Уменьшаем время на 50 мс за каждый уровень
        return max(100, base_speed - (self.level - 1) * 50)

    def new_piece(self):
        """Создает новую случайную фигуру"""
        self.current_piece = self.next_piece
        self.next_piece = Tetromino.get_random_tetromino()
        self.current_piece.x = BOARD_WIDTH // 2 - len(self.current_piece.current_shape[0]) // 2
        self.current_piece.y = 0
        
        # Проверяем, закончилась ли игра
        if self.current_piece.check_collision(self.game_board):
            self.game_over = True

    def draw_grid(self):
        """Отрисовывает сетку игрового поля"""
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                rect = pygame.Rect(
                    x * CELL_SIZE + 20,
                    y * CELL_SIZE + 20,
                    CELL_SIZE - 1,
                    CELL_SIZE - 1
                )
                pygame.draw.rect(screen, GRAY, rect, 1)

    def draw_board(self):
        """Отрисовывает все заполненные клетки на доске"""
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.game_board[y][x][1]:  # Если клетка занята
                    color = self.game_board[y][x][2]
                    rect = pygame.Rect(
                        x * CELL_SIZE + 20,
                        y * CELL_SIZE + 20,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1
                    )
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)

    def draw_current_piece(self):
        """Отрисовывает текущую падающую фигуру"""
        ghost_y = self.current_piece.get_ghost_position(self.game_board)
        
        # Отрисовка "призрака"
        for y in range(len(self.current_piece.current_shape)):
            for x in range(len(self.current_piece.current_shape[y])):
                if self.current_piece.current_shape[y][x]:
                    rect = pygame.Rect(
                        (self.current_piece.x + x) * CELL_SIZE + 20,
                        (ghost_y + y) * CELL_SIZE + 20,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1
                    )
                    pygame.draw.rect(screen, GHOST_COLOR, rect, 1)
        
        # Отрисовка самой фигуры
        for y in range(len(self.current_piece.current_shape)):
            for x in range(len(self.current_piece.current_shape[y])):
                if self.current_piece.current_shape[y][x]:
                    rect = pygame.Rect(
                        (self.current_piece.x + x) * CELL_SIZE + 20,
                        (self.current_piece.y + y) * CELL_SIZE + 20,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1
                    )
                    pygame.draw.rect(screen, self.current_piece.color, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)

    def draw_sidebar(self):
        """Отрисовывает боковую панель с информацией"""
        sidebar_x = BOARD_WIDTH * CELL_SIZE + 30
        
        # Отрисовка следующей фигуры
        next_text = font.render("Следующая:", True, WHITE)
        screen.blit(next_text, (sidebar_x, 30))
        
        # Отрисовка следующей фигуры
        for y in range(len(self.next_piece.current_shape)):
            for x in range(len(self.next_piece.current_shape[y])):
                if self.next_piece.current_shape[y][x]:
                    rect = pygame.Rect(
                        sidebar_x + x * CELL_SIZE,
                        70 + y * CELL_SIZE,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1
                    )
                    pygame.draw.rect(screen, self.next_piece.color, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)
        
        # Отрисовка счета и уровня
        score_text = font.render(f"Счет: {self.score}", True, WHITE)
        level_text = font.render(f"Уровень: {self.level}", True, WHITE)
        lines_text = font.render(f"Линии: {self.lines_cleared}", True, WHITE)
        
        screen.blit(score_text, (sidebar_x, 150))
        screen.blit(level_text, (sidebar_x, 180))
        screen.blit(lines_text, (sidebar_x, 210))
        
        # Отрисовка управления
        controls = [
            "Управление:",
            "← → - Движение",
            "↑ - Поворот",
            "↓ - Ускорить",
            "Пробел - Сбросить",
            "P - Пауза"
        ]
        
        for i, line in enumerate(controls):
            text = font.render(line, True, WHITE)
            screen.blit(text, (sidebar_x, 280 + i * 30))

    def update(self):
        """Обновляет состояние игры"""
        if self.game_over or self.paused:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall > self.fall_speed:
            if not self.current_piece.move(self.game_board, 0, 1):
                self.lock_piece()
            self.last_fall = current_time

    def lock_piece(self):
        """Фиксирует фигуру на доске и создает новую"""
        self.current_piece.place_on_board(self.game_board)
        self.game_board, lines_cleared = self.board.clear_lines(self.game_board)
        
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self.score += lines_cleared * lines_cleared * 100 * self.level
            new_level = self.lines_cleared // 10 + 1
            
            if new_level > self.level:
                self.level = new_level
                self.fall_speed = self.calculate_fall_speed()
        
        self.new_piece()

    def handle_events(self):
        """Обрабатывает события игры"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if self.game_over:
                    if event.key == K_r:
                        self.__init__()  # Перезапуск игры
                    continue
                
                if event.key == K_p:
                    self.paused = not self.paused
                
                if self.paused:
                    continue
                
                if event.key == K_LEFT:
                    self.current_piece.move(self.game_board, -1, 0)
                elif event.key == K_RIGHT:
                    self.current_piece.move(self.game_board, 1, 0)
                elif event.key == K_DOWN:
                    if not self.current_piece.move(self.game_board, 0, 1):
                        self.lock_piece()
                elif event.key == K_UP:
                    self.current_piece.rotate(self.game_board)
                elif event.key == K_SPACE:
                    self.current_piece.hard_drop(self.game_board)
                    self.lock_piece()

    def draw(self):
        """Отрисовывает все элементы игры"""
        screen.fill(BLACK)
        
        # Отрисовка игрового поля
        pygame.draw.rect(
            screen, 
            (30, 30, 30), 
            (15, 15, BOARD_WIDTH * CELL_SIZE + 10, BOARD_HEIGHT * CELL_SIZE + 10)
        )
        
        self.draw_grid()
        self.draw_board()
        self.draw_current_piece()
        self.draw_sidebar()
        
        # Отрисовка сообщения о паузе
        if self.paused:
            pause_text = font.render("ПАУЗА", True, WHITE)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(pause_text, text_rect)
        
        # Отрисовка сообщения о конце игры
        if self.game_over:
            game_over_text = font.render("ИГРА ОКОНЧЕНА", True, (255, 0, 0))
            restart_text = font.render("Нажмите R для рестарта", True, WHITE)
            
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
            screen.blit(game_over_text, text_rect)
            
            text_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10))
            screen.blit(restart_text, text_rect)
        
        pygame.display.flip()

    def run(self):
        """Основной игровой цикл"""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()