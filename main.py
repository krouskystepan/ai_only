import pygame
import sys
from board import Board

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 850  # Adjust height to accommodate text
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def main():
    clock = pygame.time.Clock()
    board = Board()
    selected_piece = None
    turn = "RED"  # Red goes first
    font = pygame.font.Font(None, 36)
    run = True
    must_capture = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = board.get_row_col_from_mouse(pos)
                print(f"Clicked position: {pos} -> Board position: {(row, col)}")  # Debug statement
                if selected_piece:
                    if board.valid_move(selected_piece, row, col):
                        if board.move_piece(selected_piece, row, col):
                            if board.has_capture_moves(selected_piece):
                                must_capture = True
                                print(f"{turn} must capture again.")  # Debug statement
                            else:
                                must_capture = False
                                turn = "BLACK" if turn == "RED" else "RED"
                        else:
                            must_capture = False
                            turn = "BLACK" if turn == "RED" else "RED"
                        selected_piece = None
                        print(f"Piece moved to: {(row, col)}")  # Debug statement
                    else:
                        selected_piece = None  # Deselect if move is invalid
                        print("Invalid move")  # Debug statement
                elif board.is_valid_selection(row, col, turn):
                    selected_piece = board.board[row][col]
                    print(f"Selected piece: {selected_piece}")  # Debug statement

        screen.fill(WHITE)
        # Display turn text
        text = font.render(f"{turn}'s turn", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, 25))
        screen.blit(text, text_rect)

        board.draw(screen, 50)  # Draw the board below the text

        if selected_piece:
            pygame.draw.rect(screen, BLUE, (selected_piece.col * SQUARE_SIZE, selected_piece.row * SQUARE_SIZE + 50, SQUARE_SIZE, SQUARE_SIZE), 4)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()