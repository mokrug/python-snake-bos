import pygame
import sys
import time
from game.settings import *
from game.snake import Snake
from game.food import Food

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.last_move_time = time.time()
        self.move_delay = 0.15  # Delay between moves in seconds
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.last_move_time = time.time()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    return

                if event.key == pygame.K_UP and self.snake.direction != DOWN:
                    self.snake.direction = UP
                elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                    self.snake.direction = DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                    self.snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                    self.snake.direction = RIGHT

    def update(self):
        if not self.game_over:
            current_time = time.time()
            if current_time - self.last_move_time >= self.move_delay:
                new_head = self.snake.move()
                self.last_move_time = current_time
                
                # Check collisions
                if self.snake.check_collision(new_head):
                    self.game_over = True
                    return

                # Check food collision
                if new_head == self.food.position:
                    self.score += 1
                    self.snake.grow()
                    self.food.respawn(self.snake.positions)
                    # Optional: Increase speed as score increases
                    self.move_delay = max(0.05, 0.15 - (self.score * 0.005))

    def draw(self):
        self.screen.fill(BLACK)
        
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render(
                'Game Over! Press SPACE to restart', 
                True, 
                WHITE
            )
            text_rect = game_over_text.get_rect(
                center=(WINDOW_SIZE/2, WINDOW_SIZE/2)
            )
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS) 