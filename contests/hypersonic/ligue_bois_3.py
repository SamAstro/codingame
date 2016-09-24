#!/opt/local/bin/python
"""
BOT FOR LIGUE BOIS 3 OF HYPERSONIC CONTEST

Version:    1.0
Created:    09/25/2016
Compiler:   python3.5

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Notes: 
"""
import sys
import math
import numpy as np


## Functions

def find_crates(idx, hero):
    ndim = len(idx[0])
    cx, cy = None, None
    
    min_dist = 1.e5
    
    for n in range(ndim):
        dx,dy = distance(hero, idx[1][n], idx[0][n])
        dist = math.sqrt(dx**2 + dy**2)
        if dist < min_dist:
            cx = idx[1][n]
            cy = idx[0][n]
            min_dist = dist
    return cx, cy
    
    
def distance(hero, cx, cy):
    distx = math.sqrt((cx - hero.x)**2)
    disty = math.sqrt((cy - hero.y)**2)
    return distx, disty

# Creating Class entity
class entity:
    def __init__(self, entity_type, owner, x, y, param_1, param_2):
        self.entity_type = entity_type
        self.owner = owner
        self.x = float(x)
        self.y = float(y)
        self.param_1 = param_1
        self.param_2 = param_2
    
def main(argv):
    # Dictionary saving the entities
    entity_dict = {}

    # Variable saving my index in the dictionary
    myidx = None

    # Auto-generated code below aims at helping you parse
    # the standard input according to the problem statement.

    width, height, my_id = [int(i) for i in input().split()]

    # Saving the grid in a matrix
    grid = np.array([['.' for j in range(width)] for i in range(height)])

    # game loop
    while True:
        for i in range(height):
            row = input()
            # Populating the grid
            for j in range(width):
                grid[i,j] = row[j]
                
        # Find the indices of all left crates
        idx = np.where(grid == "0")
        
        # Entities
        entities = int(input())
        for i in range(entities):
            entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
            # Populating the entity dictionary
            entity_dict[i] = entity(entity_type, owner, x, y, param_1, param_2)
            if entity_type == 0 and owner == my_id:
                myidx = i

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)
        
        # Find which crate is closest to me
        cx, cy = find_crates(idx, entity_dict[myidx])
        
        distx, disty = distance(entity_dict[myidx], cx, cy)
        
        print(entity_dict[myidx].x, entity_dict[myidx].y, cx, cy, distx, disty, sep=" ", file=sys.stderr)
        
        if (entity_dict[myidx].x == cx and disty <= 3) or (entity_dict[myidx].y == cy and distx <= 3):
            if entity_dict[myidx].param_1 == 1:
                # Bomb closest crate
                print("BOMB", cx, cy, sep=" ")
            else:
                print("MOVE", cx+5, cy+5, sep=" ")
        else:
            # Move to the closest crate
            print("MOVE", cx, cy, sep=" ")


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

