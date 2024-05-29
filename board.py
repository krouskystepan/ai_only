import pygame
from piece import Piece

ROWS, COLS = 8, 8
SQUARE_SIZE = 800 // COLS
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

class Board:
    def __init__(self):
        self.board = self.create_board()
        print("Board created")  # Debug statement
        self.print_board_state()  # Print initial board state

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

    def print_board_state(self):
        for row in self.board:
            print([str(piece) if piece != 0 else 0 for piece in row])

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
            print(f"Invalid position: {(row, col)}")  # Debug statement
            return False
        piece = self.board[row][col]
        if piece == 0:
            print(f"No piece at: {(row, col)}")  # Debug statement
            return False
        valid = (piece.color == RED and turn == "RED") or (piece.color == BLACK and turn == "BLACK")
        print(f"Selection at {(row, col)} is {'valid' if valid else 'invalid'} for turn {turn}")  # Debug statement
        return valid

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
                print(f"Captured piece: {self.board[mid_row][mid_col]} at {(mid_row, mid_col)}")  # Debug statement
                return True
        return False

    def move_piece(self, piece, row, col):
        mid_row = (row + piece.row) // 2
        mid_col = (col + piece.col) // 2
        captured = None
        if abs(row - piece.row) == 2 and abs(col - piece.col) == 2:
            captured = self.board[mid_row][mid_col]
            self.board[mid_row][mid_col] = 0
            print(f"{piece.color} captured {captured.color} at {(mid_row, mid_col)}")  # Debug statement
        self.board[piece.row][piece.col] = 0
        piece.move(row, col)
        if row == 0 or row == ROWS - 1:
            piece.make_king()
        self.board[row][col] = piece
        return captured is not None  # Return whether a capture occurred

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