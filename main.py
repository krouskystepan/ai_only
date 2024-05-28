import pygame
import sys

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# RGB Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def draw_board(screen):
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                pygame.draw.rect(screen, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen):
    for row in range(ROWS):
        for col in range(COLS):
            if row < 3 and (row + col) % 2 == 1:
                pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10)
            elif row > 4 and (row + col) % 2 == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10)

def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_board(screen)
        draw_pieces(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()