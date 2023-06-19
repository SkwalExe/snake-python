from distutils.spawn import spawn
from random import randint
from colors import *
from os import system
from sys import stdout

BORDER = f'{BG_PURPLE}  {RESET}'
SNAKE = f'{BG_WHITE}  {RESET}'
FOOD = f'{BG_RED}  {RESET}'
EMPTY = f'  '

class MatrixChange:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

class Matrix:
    def __init__(self):
        self.changes = []
        # clear the termimnal
        system("clear")
    
    def print_at(self, x, y, value):
        print(f"\033[{y + 1};{x * 2 + 1}H{value}", end="")

    def update(self, x, y, value):
        self.changes.append(MatrixChange(x, y, value))

    def draw(self):
        for change in self.changes:
            self.print_at(change.x, change.y, change.value)
        self.changes = []
        stdout.flush()


class Game:
    def spawn_food(self):
        # 1, -2 to avoid the borders
        pos = (randint(1, self.width - 2), randint(1, self.height - 2))
        # If there is already food at the position then try again
        if not pos in self.foods:
            self.foods.append(pos)
            self.matrix.update(pos[0], pos[1], FOOD)
        else:
            self.spawn_food()


    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = Matrix()
        self.snake = [(width // 2 + 1, height // 2), (width // 2, height // 2), (width // 2 - 1, height // 2)]
        self.foods = []
        self.spawn_food()
        self.direction = 'right'
        self.original_direction = 'right'
        self.score = 0
        self.game_over = False

        # Draw borders
        for x in range(width):
            self.matrix.update(x, 0, BORDER)
            self.matrix.update(x, height - 1, BORDER)

        for y in range(height):
            self.matrix.update(0, y, BORDER)
            self.matrix.update(width - 1, y, BORDER)
        
        self.matrix.draw()

    def set_direction(self, direction):
        if direction == 'up' and self.original_direction != 'down':
            self.direction = direction
        elif direction == 'down' and self.original_direction != 'up':
            self.direction = direction
        elif direction == 'left' and self.original_direction != 'right':
            self.direction = direction
        elif direction == 'right' and self.original_direction != 'left':
            self.direction = direction

    def draw(self):
        self.matrix.draw()
        # spaces at the end to clear the "Paused" text
        self.matrix.print_at(0, self.height, f"Score: {self.score}\n      ")

    def update(self):
        # add the new head to the snake
        self.original_direction = self.direction
        head = self.snake[0]
        if self.direction == 'up':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'down':
            new_head = (head[0], head[1] + 1)
        elif self.direction == 'left':
            new_head = (head[0] - 1, head[1])
        elif self.direction == 'right':
            new_head = (head[0] + 1, head[1])
        # check if the snake is out of bounds
        if new_head[0] <= 0 or new_head[0] >= self.width - 1 or new_head[1] <= 0 or new_head[1] >= self.height - 1:
            return self.end()

        # check if the snake has collided with itself
        if new_head in self.snake:
            return self.end()

        self.snake.insert(0, new_head)
        self.matrix.update(new_head[0], new_head[1], SNAKE)

        # if one of the cells of the snake is on the food then dont remove the last element of the snake
        found_food = False
        for food in self.foods:
            if food in self.snake:
                self.score += 1
                self.foods.remove(food)
                # no need to erase the food since the snake will be drawn over it
                if len(self.foods) == 0:
                    self.spawn_food()
                found_food = True
        if not found_food:
            self.matrix.update(self.snake[-1][0], self.snake[-1][1], EMPTY)
            self.snake = self.snake[:-1]

        return True

    def end(self):
        self.game_over = True
        print("\rYou lost!")
        return False