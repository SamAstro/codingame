#!/opt/local/bin/python
"""
DESCRIPTION OF THE SCRIPT

Version: 1.0
Created: 09/21/2016
Compiler: python

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Notes: 
"""
import sys
import math

def main(argv):
    # The while loop represents the game.
    # Each iteration represents a turn of the game
    # where you are given inputs (the heights of the mountains)
    # and where you have to print an output (the index of the mountain to fire on)
    # The inputs you are given are automatically updated according to your last actions.


    # game loop
    while True:
        target_h = 0
        target_idx = 0
        for i in range(8):
            mountain_h = int(input())  # represents the height of one mountain.
            if mountain_h > target_h:
                target_h = mountain_h
                target_idx = i
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        # The index of the mountain to fire on.
        print(target_idx)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

