import pygame
import sys
from game import Game

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 850  # Adjust height to accommodate text
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def main():
    clock = pygame.time.Clock()
    game = Game(screen)
    font = pygame.font.Font(None, 36)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.select(pos)

        screen.fill(WHITE)
        # Display turn text
        text = font.render(f"{game.turn}'s turn", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, 25))
        screen.blit(text, text_rect)

        game.update()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
