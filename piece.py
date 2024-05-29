import pygame

SQUARE_SIZE = 800 // 8
GREY = (128, 128, 128)
BLUE = (0, 0, 255)

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def move(self, row, col):
        self.row = row
        self.col = col

    def make_king(self):
        self.king = True

    def draw(self, screen, offset):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(screen, GREY, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2 + offset), radius + self.OUTLINE)
        pygame.draw.circle(screen, self.color, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2 + offset), radius)
        if self.king:
            pygame.draw.circle(screen, BLUE, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2 + offset), radius // 2)

    def __repr__(self):
        return f"Piece({self.row}, {self.col}, {'RED' if self.color == (255, 0, 0) else 'BLACK'})"
