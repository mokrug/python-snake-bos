import random
import pygame
from game.settings import *

class Food:
    def __init__(self):
        self.position = self.get_random_position()

    def get_random_position(self):
        return (
            random.randint(0, GRID_COUNT-1),
            random.randint(0, GRID_COUNT-1)
        )

    def respawn(self, snake_positions):
        self.position = self.get_random_position()
        while self.position in snake_positions:
            self.position = self.get_random_position()

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            RED,
            (self.position[0]*GRID_SIZE, 
             self.position[1]*GRID_SIZE,
             GRID_SIZE-1, GRID_SIZE-1)
        ) 