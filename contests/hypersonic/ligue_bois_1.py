#!/opt/local/bin/python
"""
DESCRIPTION OF THE SCRIPT

Version:    0.5
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
    cx,cy = None, None
    min_dist = 1.e5
    #mdx = 1.e5
    #mdy = 1.e5
    
    if ndim == 0:
        cx, cy = 0,0
    else:
        for n in range(ndim):
            dx,dy = distance(hero, idx[1][n], idx[0][n])
            dist = math.sqrt(dx**2 + dy**2)
            if dist < min_dist:
                #if dx < mdx:
                cx = idx[1][n]
                    #mdx = cx
                #if dy < mdy:
                cy = idx[0][n]
                    #mdy = cy
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
        self.x = int(x)
        self.y = int(y)
        self.param_1 = param_1
        self.param_2 = param_2
    

        
def main(argv):
    # Dictionary saving the entities
    entity_dict = {}

    # Variable saving my index in the dictionary
    myidx = None
    oidx = None
    # Bomb reach initialized to 3 squares
    bomb_reach = 3

    # Offset
    xoffset = 5
    yoffset = 5

    # Hero position
    hx, hy = None, None

    # Auto-generated code below aims at helping you parse
    # the standard input according to the problem statement.

    width, height, my_id = [int(i) for i in input().split()]
    print("my id:", my_id, file=sys.stderr)

    # Saving the grid in a matrix
    grid = np.array([['.' for j in range(width)] for i in range(height)])

    # game loop
    while True:
        for i in range(height):
            row = input()
            # Populating the grid
            for j in range(width):
                grid[i,j] = row[j]
                
        idx = np.where(np.logical_and(grid != ".", grid != 'X'))
        
        # Entities
        entities = int(input())
        for i in range(entities):
            entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
            # Populating the entity dictionary
            entity_dict[i] = entity(entity_type, owner, x, y, param_1, param_2)
            if entity_type == 0 and owner == my_id:
                myidx = i
                hx = x
                hy = y
            if entity_type == 2:
                dohx, dohy = distance(entity_dict[myidx], x, y)
                doh = math.sqrt(dohx**2 + dohy**2)
                print(x,y,dohx,dohy, file=sys.stderr)
                if (dohx < 1 or dohy < 1) and doh < 3:
                    oidx = i
                else:
                    oidx = None
            if entity_type == 1 and owner == my_id:
                bomb_reach = param_2-1
            
        if oidx == None:
            print("moving...", file=sys.stderr)
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr)
            
            # Find which crate is closest to me
            cx, cy = find_crates(idx, entity_dict[myidx])
            
            distx, disty = distance(entity_dict[myidx], cx, cy)
            
            print(entity_dict[myidx].x, entity_dict[myidx].y, cx, cy, distx, disty, sep=" ", file=sys.stderr)
            
            if (disty < bomb_reach or distx < bomb_reach):
                if entity_dict[myidx].param_1 != 0:
                    # Bomb closest crate
                    print("BOMB", cx, cy, sep=" ")
                else:
                    xoffset = 5 if entity_dict[myidx].x+xoffset < width-1 else -5
                    yoffset = 5 if entity_dict[myidx].y+yoffset < height-1 else -5
                    print("MOVE", entity_dict[myidx].x+xoffset, entity_dict[myidx].y+yoffset, sep=" ")
            else:
                # Move to the closest crate
                print("MOVE", cx, cy, sep=" ")
        else:
            print("UPs! UPs! UPs!", file=sys.stderr)
            print("MOVE", entity_dict[oidx].x, entity_dict[oidx].y, sep=" ")
            oidx = None
            

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

