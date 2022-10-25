from distutils.spawn import spawn
from random import randint
from colors import *

class Game:
    def spawn_food(self):
        pos = (randint(0, self.width - 1), randint(0, self.height - 1))
        if not pos in self.foods:
            self.foods.append(pos)
        else:
            self.spawn_food()

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = [(width // 2 + 1, height // 2), (width // 2, height // 2), (width // 2 - 1, height // 2)]
        self.foods = []
        self.spawn_food()
        self.direction = 'right'
        self.original_direction = 'right'
        self.score = 0
        self.game_over = False


    def print(self):
        # clear the termimnal
        print('\033[1;1H\033[2J', end='')
        # print the score
        print(f'Score: {self.score}')
        for y in range(-1, self.height +1):
            for x in range(-1, self.width+1):
                # draw borders
                if x == -1 or x == self.width or y == -1 or y == self.height:
                    print(BG_PURPLE + '  ' + RESET, end='')
                elif (x, y) in self.snake:
                    print(f'{BG_WHITE}  {RESET}', end='')
                elif (x, y) in self.foods:
                    print(f'{BG_RED}  {RESET}', end='')
                else:
                    print('  ', end='')
            print()

    def set_direction(self, direction):
        if direction == 'up' and self.original_direction != 'down':
            self.direction = direction
        elif direction == 'down' and self.original_direction != 'up':
            self.direction = direction
        elif direction == 'left' and self.original_direction != 'right':
            self.direction = direction
        elif direction == 'right' and self.original_direction != 'left':
            self.direction = direction

    def update(self):
        # check if the player won the game
        if len(self.snake) == self.width * self.height:
            self.end(True)
            return
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
        if new_head[0] < 0 or new_head[0] >= self.width or new_head[1] < 0 or new_head[1] >= self.height:
            return self.end()

        # check if the snake has collided with itself
        if new_head in self.snake:
            return self.end()

        self.snake.insert(0, new_head)

        # if one of the cells of the snake is on the food then dont remove the last element of the snake
        found_food = False
        for food in self.foods:
            if food in self.snake:
                self.score += 1
                self.foods.remove(food)
                if len(self.foods) == 0:
                    self.spawn_food()
                found_food = True
        if not found_food:
            self.snake = self.snake[:-1]


    def end(self, won=False):
        self.game_over = True
        if won:
            print("You won!")
        else:
            print("Game Over!")
        print(f"Your score: {self.score}")
