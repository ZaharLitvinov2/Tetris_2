import pygame
from copy import deepcopy
import sounds

class Board:
    """Класс игрового поля для тетриса"""
    
    def __init__(self, width, height):
        """Инициализация игрового поля
        Args:
            width: ширина поля в клетках
            height: высота поля в клетках
        """
        self.width = width
        self.height = height
        self.cell_size = 30  # Размер клетки в пикселях
        self.left = 20  # Отступ слева
        self.top = 20   # Отступ сверху
    
    def create(self):
        """Создает пустое игровое поле"""
        board = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Каждая клетка содержит:
                # 0 - координаты (x, y)
                # 1 - занята ли клетка (True/False)
                # 2 - цвет (если клетка занята)
                cell = [
                    (x * self.cell_size + self.left, 
                     y * self.cell_size + self.top),
                    False  # По умолчанию клетка свободна
                ]
                row.append(cell)
            board.append(row)
        return board
    
    def clear_lines(self, board):
        """Удаляет заполненные линии и возвращает новое состояние поля
        Args:
            board: текущее состояние игрового поля
        Returns:
            new_board: обновленное поле
            lines_cleared: количество удаленных линий
        """
        # Находим незаполненные строки
        new_board = [row for row in board if not all(cell[1] for cell in row)]
        lines_cleared = self.height - len(new_board)
        if lines_cleared > 0:
            sounds.play_broken_sequence()
        # Добавляем новые пустые строки сверху
        for _ in range(lines_cleared):
            new_row = []
            for x in range(self.width):
                new_row.append([
                    (x * self.cell_size + self.left, 
                     self.top),
                    False
                ])
            new_board.insert(0, new_row)
        
        # Обновляем координаты всех клеток
        for y in range(self.height):
            for x in range(self.width):
                new_board[y][x][0] = (
                    x * self.cell_size + self.left,
                    y * self.cell_size + self.top
                )
        
        return new_board, lines_cleared