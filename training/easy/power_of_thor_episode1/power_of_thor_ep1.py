#!/opt/local/bin/python
"""
DESCRIPTION OF THE SCRIPT

Version: 1.0
Created: 09/21/2016
Compiler: python 3.5

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Notes: 
"""
import sys
import math

def main(argv):
    # Auto-generated code below aims at helping you parse
    # the standard input according to the problem statement.
    # ---
    # Hint: You can use the debug stream to print initialTX and initialTY, if Thor seems not follow your orders.

    # light_x: the X position of the light of power
    # light_y: the Y position of the light of power
    # initial_tx: Thor's starting X position
    # initial_ty: Thor's starting Y position
    light_x, light_y, initial_tx, initial_ty = [int(i) for i in input().split()]
    pos_tx = initial_tx
    pos_ty = initial_ty

    # game loop
    while True:
        remaining_turns = int(input())  # The remaining amount of turns Thor can move. Do not remove this line.

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)
        direction_x = pos_tx - light_x
        direction_y = pos_ty - light_y
        direction = ""
        
        if direction_y > 0:
            direction += "N"
            pos_ty -= 1
        elif direction_y < 0:
            direction += "S"
            pos_ty += 1
        else:
            pass
        
        if direction_x > 0:
            direction += "W"
            pos_tx -= 1
        elif direction_x < 0:
            direction += "E"
            pos_tx += 1
        else:
            pass
        
        # A single line providing the move to be made: N NE E SE S SW W or NW
        print(direction)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

