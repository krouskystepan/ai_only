import pygame
from piece import Piece

ROWS, COLS = 8, 8
SQUARE_SIZE = 800 // COLS
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = []
        for row in range(ROWS):
            board.append([])
            for col in range(COLS):
                if row % 2 == (col % 2):
                    if row < 3:
                        board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        board[row].append(Piece(row, col, RED))
                    else:
                        board[row].append(0)
                else:
                    board[row].append(0)
        return board

    def draw(self, screen, offset):
        self.draw_squares(screen, offset)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen, offset)

    def draw_squares(self, screen, offset):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(screen, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE + offset, SQUARE_SIZE, SQUARE_SIZE))

    def draw_valid_moves(self, screen, moves, offset):
        for move in moves:
            row, col = move
            pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + offset), 15)

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        y = y - 50  # Adjust for offset
        if y < 0:
            return -1, -1  # Invalid position due to offset
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        if row < 0 or col < 0 or row >= ROWS or col >= COLS:
            return -1, -1  # Invalid position
        return row, col

    def is_valid_selection(self, row, col, turn):
        if row < 0 or row >= ROWS or col < 0 or col >= COLS:
            return False
        piece = self.board[row][col]
        if piece == 0:
            return False
        return (piece.color == RED and turn == "RED") or (piece.color == BLACK and turn == "BLACK")

    def valid_move(self, piece, row, col):
        if row < 0 or row >= ROWS or col < 0 or col >= COLS:
            return False
        if self.board[row][col] != 0:
            return False
        if piece.color == RED or piece.king:
            if row - piece.row == -1 and abs(col - piece.col) == 1:
                return True
        if piece.color == BLACK or piece.king:
            if row - piece.row == 1 and abs(col - piece.col) == 1:
                return True
        if abs(row - piece.row) == 2 and abs(col - piece.col) == 2:
            mid_row = (row + piece.row) // 2
            mid_col = (col + piece.col) // 2
            if self.board[mid_row][mid_col] != 0 and self.board[mid_row][mid_col].color != piece.color:
                return True
        return False

    def move_piece(self, piece, row, col):
        captured_pieces = []
        if abs(row - piece.row) == 2 and abs(col - piece.col) == 2:
            mid_row = (row + piece.row) // 2
            mid_col = (col + piece.col) // 2
            captured_piece = self.board[mid_row][mid_col]
            self.board[mid_row][mid_col] = 0
            captured_pieces.append((mid_row, mid_col))
        self.board[piece.row][piece.col] = 0
        piece.move(row, col)
        if row == 0 or row == ROWS - 1:
            piece.make_king()
        self.board[row][col] = piece
        return captured_pieces

    def get_all_valid_moves(self, piece):
        moves = {}
        for row in range(ROWS):
            for col in range(COLS):
                if self.valid_move(piece, row, col):
                    moves[(row, col)] = self.board[row][col]
        return moves

    def has_capture_moves(self, piece):
        for row in range(ROWS):
            for col in range(COLS):
                if abs(row - piece.row) == 2 and abs(col - piece.col) == 2:
                    if self.valid_move(piece, row, col):
                        return True
        return False

    def get_capture_paths(self, piece):
        def dfs(current_piece, path, visited):
            capture_paths = []
            moves = self.get_all_valid_moves(current_piece)
            for move in moves:
                row, col = move
                if abs(row - current_piece.row) == 2 and abs(col - current_piece.col) == 2:
                    mid_row = (row + current_piece.row) // 2
                    mid_col = (col + current_piece.col) // 2
                    if (mid_row, mid_col) not in visited:
                        new_piece = Piece(row, col, current_piece.color)
                        new_piece.king = current_piece.king
                        new_path = path + [(row, col)]
                        new_visited = visited.copy()
                        new_visited.add((mid_row, mid_col))
                        sub_paths = dfs(new_piece, new_path, new_visited)
                        if sub_paths:
                            capture_paths.extend(sub_paths)
                        else:
                            capture_paths.append(new_path)
            if not capture_paths:
                capture_paths.append(path)
            return capture_paths

        paths = dfs(piece, [], set())
        paths = [path for path in paths if path]  # Filter out empty paths
        if not paths:
            return []
        max_length = max(len(path) for path in paths)
        return [path for path in paths if len(path) == max_length]
