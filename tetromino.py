import random
from copy import deepcopy

class Tetromino:
    """Класс для работы с фигурами тетриса"""
    
    SHAPES = {
        'I': [
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
            
            [[0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0]],
            
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0]],
            
            [[0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]]
        ],
        'O': [
            [[1, 1],
             [1, 1]]
        ],
        'T': [
            [[0, 1, 0],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[0, 1, 0],
             [0, 1, 1],
             [0, 1, 0]],
            
            [[0, 0, 0],
             [1, 1, 1],
             [0, 1, 0]],
            
            [[0, 1, 0],
             [1, 1, 0],
             [0, 1, 0]]
        ],
        'L': [
            [[0, 0, 1],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[0, 1, 0],
             [0, 1, 0],
             [0, 1, 1]],
            
            [[0, 0, 0],
             [1, 1, 1],
             [1, 0, 0]],
            
            [[1, 1, 0],
             [0, 1, 0],
             [0, 1, 0]]
        ],
        'J': [
            [[1, 0, 0],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[0, 1, 1],
             [0, 1, 0],
             [0, 1, 0]],
            
            [[0, 0, 0],
             [1, 1, 1],
             [0, 0, 1]],
            
            [[0, 1, 0],
             [0, 1, 0],
             [1, 1, 0]]
        ],
        'S': [
            [[0, 1, 1],
             [1, 1, 0],
             [0, 0, 0]],
            
            [[0, 1, 0],
             [0, 1, 1],
             [0, 0, 1]],
            
            [[0, 0, 0],
             [0, 1, 1],
             [1, 1, 0]],
            
            [[1, 0, 0],
             [1, 1, 0],
             [0, 1, 0]]
        ],
        'Z': [
            [[1, 1, 0],
             [0, 1, 1],
             [0, 0, 0]],
            
            [[0, 0, 1],
             [0, 1, 1],
             [0, 1, 0]],
            
            [[0, 0, 0],
             [1, 1, 0],
             [0, 1, 1]],
            
            [[0, 1, 0],
             [1, 1, 0],
             [1, 0, 0]]
        ]
    }
    
    COLORS = {
        'I': (0, 255, 255),   # Голубой
        'O': (255, 255, 0),   # Желтый
        'T': (128, 0, 128),   # Фиолетовый
        'L': (255, 165, 0),   # Оранжевый
        'J': (0, 0, 255),     # Синий
        'S': (0, 255, 0),     # Зеленый
        'Z': (255, 0, 0)      # Красный
    }

    def __init__(self, shape_type):
        self.shape_type = shape_type
        self.rotations = deepcopy(self.SHAPES[shape_type])
        self.rotation_index = 0
        self.current_shape = self.rotations[self.rotation_index]
        self.color = self.COLORS[shape_type]
        self.x = 0
        self.y = 0

    def rotate(self, board):
        if self.shape_type == 'O':
            return False
        
        old_shape = self.current_shape
        old_index = self.rotation_index
        
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)
        self.current_shape = self.rotations[self.rotation_index]
        
        if self.check_collision(board):
            self.current_shape = old_shape
            self.rotation_index = old_index
            return False
        
        return True

    def check_collision(self, board):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[y])):
                if self.current_shape[y][x]:
                    board_x = self.x + x
                    board_y = self.y + y
                    
                    if (board_x < 0 or board_x >= len(board[0]) or 
                        board_y >= len(board)):
                        return True
                    
                    if board_y >= 0 and board[board_y][board_x][1]:
                        return True
        return False

    def place_on_board(self, board):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[y])):
                if self.current_shape[y][x]:
                    board_y = self.y + y
                    board_x = self.x + x
                    if 0 <= board_y < len(board) and 0 <= board_x < len(board[0]):
                        board[board_y][board_x][1] = True
                        if len(board[board_y][board_x]) == 2:
                            board[board_y][board_x].append(self.color)
                        else:
                            board[board_y][board_x][2] = self.color

    def remove_from_board(self, board):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[y])):
                if self.current_shape[y][x]:
                    board_y = self.y + y
                    board_x = self.x + x
                    if 0 <= board_y < len(board) and 0 <= board_x < len(board[0]):
                        board[board_y][board_x][1] = False

    def move(self, board, dx, dy):
        self.x += dx
        self.y += dy
        
        if self.check_collision(board):
            self.x -= dx
            self.y -= dy
            return False
        
        return True

    def hard_drop(self, board):
        while self.move(board, 0, 1):
            pass

    def get_ghost_position(self, board):
        ghost_y = self.y
        while True:
            ghost_y += 1
            collision = False
            for y in range(len(self.current_shape)):
                for x in range(len(self.current_shape[y])):
                    if self.current_shape[y][x]:
                        board_x = self.x + x
                        board_y = ghost_y + y
                        
                        if (board_y >= len(board) or 
                            (board_y >= 0 and board[board_y][board_x][1])):
                            collision = True
                            break
                if collision:
                    break
            
            if collision:
                ghost_y -= 1
                break
        
        return ghost_y

    @classmethod
    def get_random_tetromino(cls):
        shapes = ['I', 'O', 'T', 'L', 'J', 'S', 'Z']
        return cls(random.choice(shapes))