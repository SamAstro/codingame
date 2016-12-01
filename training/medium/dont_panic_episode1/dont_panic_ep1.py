#!/opt/local/bin/python
"""
SOLUTION TO THE 'DONT PANIC EP1' PUZZLE

Version:
Created:
Compiler: python

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Affiliation:
Notes: 
"""
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# nb_floors: number of floors
# width: width of the area
# nb_rounds: maximum number of rounds
# exit_floor: floor on which the exit is found
# exit_pos: position of the exit on its floor
# nb_total_clones: number of generated clones
# nb_additional_elevators: ignore (always zero)
# nb_elevators: number of elevators
nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for i in input().split()]

elevators = [None for i in range(nb_elevators)]

for i in range(nb_elevators):
    # elevator_floor: floor on which this elevator is found
    # elevator_pos: position of the elevator on its floor
    elevator_floor, elevator_pos = [int(j) for j in input().split()]
    # Filling elevator list
    elevators[elevator_floor] = elevator_pos

# game loop
while True:
    # clone_floor: floor of the leading clone
    # clone_pos: position of the leading clone on its floor
    # direction: direction of the leading clone: LEFT or RIGHT
    clone_floor, clone_pos, direction = input().split()
    clone_floor = int(clone_floor)
    clone_pos = int(clone_pos)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # action: WAIT or BLOCK
    
    if clone_floor == -1:
        print('WAIT')
    elif clone_floor == exit_floor:
        if clone_pos > exit_pos and direction == 'RIGHT':
            print('BLOCK')
        elif clone_pos < exit_pos and direction == 'LEFT':
            print('BLOCK')
        else:
            print('WAIT')
    else:
        if clone_pos > elevators[clone_floor] and direction == 'RIGHT':
            print('BLOCK')
        elif clone_pos < elevators[clone_floor] and direction == 'LEFT':
            print('BLOCK')
        else:
            print('WAIT')

