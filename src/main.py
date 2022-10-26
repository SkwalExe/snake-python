import pynput
from os import get_terminal_size, system
from time import sleep
from game import *

def hide_stdin():
    system("stty -echo")

def show_stdin():
    system("stty echo")

def main():
    hide_stdin()
    size = get_terminal_size()
    width = int(size.columns / 2 - 4)
    height = int(size.lines - 4)
    playing = True
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
                game.print()
                game.update()
            else:
                print("\rPaused", end="")
            sleep(0.1)

if __name__ == "__main__":
    main()