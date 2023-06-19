#!/usr/bin/env python3

import pynput
from os import get_terminal_size, system
from time import sleep
from game import *
import cursor

# Prevent user input from being displayed on the terminal
def hide_stdin():
    system("stty -echo")
    cursor.hide()

# Allow user input to be displayed on the terminal
def show_stdin():
    system("stty echo")
    cursor.show()

def main():
    hide_stdin()
    size = get_terminal_size()
    # Divide the width by 2 to account for the fact that a block is 2 characters wide
    # Subtract 4 from the height and width to account for the text at the top and give some space around the edges 
    width = int(size.columns / 2) 
    height = int(size.lines - 2)
    paused = False
    game = Game(width, height)
    def on_press(key):
        if key == pynput.keyboard.Key.up:
            game.set_direction('up')
        elif key == pynput.keyboard.Key.down:
            game.set_direction('down')
        elif key == pynput.keyboard.Key.left:
            game.set_direction('left')
        elif key == pynput.keyboard.Key.right:
            game.set_direction('right')
        elif key == pynput.keyboard.Key.esc:
            game.game_over = True
        elif key == pynput.keyboard.Key.space:
            nonlocal paused
            paused = not paused


    with pynput.keyboard.Listener(on_press=on_press) as listener:
        while not game.game_over:
            if not paused:
                if game.update():
                    game.draw()
            else:
                print("\rPaused", end="")
            sleep(0.1)
        print()
        show_stdin()

if __name__ == "__main__":
    main()