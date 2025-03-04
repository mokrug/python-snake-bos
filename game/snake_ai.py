from game.settings import *
from collections import deque
import heapq  # Add this import for priority queue

class SnakeAI:
    def __init__(self, game):
        self.game = game

    def get_next_move(self):
        """Returns the next optimal direction for the snake"""
        path = self.find_path_to_food()
        if not path:
            # If no path to food, try to follow tail
            path = self.find_survival_path()
            if not path:
                # If no survival path, try to make the largest possible move
                return self.find_safe_direction()
        
        if len(path) < 2:
            return self.find_safe_direction()

        # Get the next direction from the path
        next_pos = path[1]  # path[0] is current position
        current = self.game.snake.positions[0]
        return (next_pos[0] - current[0], next_pos[1] - current[1])

    def find_path_to_food(self):
        """Uses A* pathfinding to find path to food"""
        start = self.game.snake.positions[0]
        goal = self.game.food.position
        
        # Priority queue for A* algorithm
        pq = []
        heapq.heappush(pq, (0, 0, start, [start]))  # (f_score, g_score, position, path)
        visited = set()
        
        while pq:
            _, g_score, current, path = heapq.heappop(pq)
            
            if current == goal:
                return path
                
            if current in visited:
                continue
                
            visited.add(current)
            
            # Check all possible moves
            for direction in [UP, DOWN, LEFT, RIGHT]:
                next_pos = (current[0] + direction[0], current[1] + direction[1])
                
                if self.is_valid_move(next_pos, path):
                    new_path = path + [next_pos]
                    new_g = g_score + 1
                    new_f = new_g + self.manhattan_distance(next_pos, goal)
                    heapq.heappush(pq, (new_f, new_g, next_pos, new_path))
        
        return None

    def find_survival_path(self):
        """Finds a path to the snake's tail when no path to food exists"""
        start = self.game.snake.positions[0]
        goal = self.game.snake.positions[-1]
        
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            current, path = queue.popleft()
            
            if current == goal:
                return path
                
            for direction in [UP, DOWN, LEFT, RIGHT]:
                next_pos = (current[0] + direction[0], current[1] + direction[1])
                
                if self.is_valid_move(next_pos, path) and next_pos not in visited:
                    visited.add(next_pos)
                    new_path = path + [next_pos]
                    queue.append((next_pos, new_path))
        
        return None

    def find_safe_direction(self):
        """Finds a safe direction when no path exists"""
        current = self.game.snake.positions[0]
        for direction in [UP, DOWN, LEFT, RIGHT]:
            next_pos = (current[0] + direction[0], current[1] + direction[1])
            if self.is_valid_move(next_pos, [current]):
                return direction
        return self.game.snake.direction  # Keep current direction if no safe move

    def is_valid_move(self, pos, path):
        """Checks if a move is valid"""
        # Check boundaries
        if (pos[0] < 0 or pos[0] >= GRID_COUNT or 
            pos[1] < 0 or pos[1] >= GRID_COUNT):
            return False
            
        # Check collision with snake body
        snake_body = set(self.game.snake.positions)
        # Remove tail if not growing
        if len(path) <= len(snake_body):
            snake_body.remove(self.game.snake.positions[-1])
            
        return pos not in snake_body

    def manhattan_distance(self, pos1, pos2):
        """Calculates Manhattan distance between two points"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) 