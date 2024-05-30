import pygame
from board import Board

class Game:
    def __init__(self, screen):
        self.board = Board()
        self.turn = "RED"
        self.selected_piece = None
        self.valid_moves = []
        self.must_capture = False
        self.screen = screen

    def select(self, pos):
        row, col = self.board.get_row_col_from_mouse(pos)

        if self.selected_piece:
            if (row, col) in self.valid_moves:
                captured_positions = self.board.move_piece(self.selected_piece, row, col)
                for pos in captured_positions:
                    self.board.board[pos[0]][pos[1]] = 0  # Ensure captured piece is removed
                capture_paths = self.board.get_capture_paths(self.selected_piece)
                if capture_paths and len(capture_paths[0]) > 1:
                    self.must_capture = True
                    self.valid_moves = [capture_paths[0][-1]]  # Only show the final move in the longest path
                else:
                    self.must_capture = False
                    self.turn = "BLACK" if self.turn == "RED" else "RED"
                    self.valid_moves = []
                self.selected_piece = None
            else:
                self.selected_piece = None
                self.valid_moves = []
        elif self.board.is_valid_selection(row, col, self.turn):
            self.selected_piece = self.board.board[row][col]
            capture_paths = self.board.get_capture_paths(self.selected_piece)
            if capture_paths:
                self.valid_moves = [capture_paths[0][-1]]  # Only show the final move in the longest path
            else:
                self.valid_moves = list(self.board.get_all_valid_moves(self.selected_piece).keys())

    def update(self):
        offset = 50
        self.board.draw(self.screen, offset)
        if self.selected_piece:
            pygame.draw.rect(self.screen, (0, 0, 255), (self.selected_piece.col * 100, self.selected_piece.row * 100 + offset, 100, 100), 4)
            self.board.draw_valid_moves(self.screen, self.valid_moves, offset)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Checkers')
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.select(pos)

        screen.fill((255, 255, 255))
        game.update()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
