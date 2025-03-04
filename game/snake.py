import pygame
from game.settings import *

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = RIGHT
        self.length = 1

    def move(self):
        new_head = (
            self.positions[0][0] + self.direction[0],
            self.positions[0][1] + self.direction[1]
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        return new_head

    def grow(self):
        self.length += 1

    def check_collision(self, pos):
        # Check wall collision
        if (pos[0] < 0 or pos[0] >= GRID_COUNT or 
            pos[1] < 0 or pos[1] >= GRID_COUNT):
            return True
        # Check self collision
        if pos in self.positions[1:]:
            return True
        return False

    def draw(self, screen):
        for pos in self.positions:
            pygame.draw.rect(
                screen, 
                GREEN, 
                (pos[0]*GRID_SIZE, pos[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1)
            ) 