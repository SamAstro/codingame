import sys
import math
import numpy as np
import random

# Flags
isFirstTurn = True

# Reproducing randomness -- FOR DEBUG ONLY
#random.seed(9001)


# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

import numpy
from heapq import *


def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))
    
    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    # this is where you define what is wall
                    if array[neighbor[0]][neighbor[1]] == -1 or array[neighbor[0]][neighbor[1]] == 9:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return False


##### MY FUNCTIONS #####
def distance(hero, cx, cy):
    """.

    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
    """
    dx = cx - hero.x
    dy = cy - hero.y
    dist = math.fabs(dx) + math.fabs(dy)

    return dist, dx, dy



##### CLASSES #####

class MasterGrid():
    def __init__(self, grid, safety_map, crates = {}, all_bombs = {}, ups={}, bots={}):
        height,width = grid.shape
        self.width = width
        self.height = height
        self.grid = grid
        self.safety_map = safety_map
        self.crates = crates
        self.all_bombs = all_bombs
        self.ups = ups
        self.bots = bots

    def init_safety_map(self):
        for i in range(self.height):
            for j in range(self.width):
                # Reinitilizing the map
                self.safety_map[i,j] = 0

        for i in range(self.height):
            for j in range(self.width):
                # Setting to danger every tile affected by a bomb
                for k, bomb in self.all_bombs.items():
                    if bomb.x == j and bomb.y ==i:
                        # Setting row to danger
                        start = j-bomb.param_2 if  j-bomb.param_2 > 0 else 0
                        end =  j+bomb.param_2 if  j+bomb.param_2 < width else width
                        for jj in range(start, end):
                            delta = math.fabs(j-jj)
                            self.safety_map[i,jj] = 9 - delta
                        # Setting column to danger
                        start = i-bomb.param_2 if  i-bomb.param_2 > 0 else 0
                        end =  i+bomb.param_2 if  i+bomb.param_2 < height else height
                        for ii in range(start, end):
                            delta = math.fabs(i-ii)
                            self.safety_map[ii,j] = 9 - delta
        for i in range(self.height):
            for j in range(self.width):
                # Setting back walls and crates to -1
                if self.grid[i,j] != ".":
                    self.safety_map[i,j] = -1

    def simulate_safety_grid(self, bx, by, bomb_reach):
        simulated_safety_map = np.copy(self.safety_map)
         # Setting row to danger
        start = bx-bomb_reach if  bx-bomb_reach > 0 else 0
        end =  bx+bomb_reach if  bx+bomb_reach < width else width
        for j in range(start, end):
            delta = math.fabs(bx-j)
            simulated_safety_map[by,j] = 9 - delta
        # Setting column to danger
        start = by-bomb_reach if  by-bomb_reach > 0 else 0
        end =  by+bomb_reach if  by+bomb_reach < height else height
        for i in range(start, end):
            delta = math.fabs(by-i)
            simulated_safety_map[i,bx] = 9 - delta

        for i in range(self.height):
            for j in range(self.width):
                # Setting back walls and crates to -1
                if self.grid[i,j] != ".":
                    self.safety_map[i,j] = -1

        return simulated_safety_map
        


# Creating Class entity
class Entity():
    def __init__(self, entity_type=0, owner=0, x=0, y=0, param_1=0, param_2=0):
        self.entity_type = entity_type
        self.owner = owner
        self.x = int(x)
        self.y = int(y)
        self.param_1 = param_1
        self.param_2 = param_2


class Hero(Entity):
    # Saving HERO previous position
    past_x = 0
    past_y = 0
    bomb_reach = 2
    DEST = [0,0]
    next_move = [0,0]


    def __init__(self, entity_type=0, owner=0, x=0, y=0, param_1=0, param_2=0):
        super().__init__(entity_type=0, owner=0, x=0, y=0, param_1=0, param_2=0)

    # Methods related to DESTINATION
    def has_reach_destination(self):
        if hero.x == hero.DEST[0] and hero.y == hero.DEST[1]:
            return True
        else:
            return False

    def find_new_destination(self, master_grid):
        # Is there UPs or CRATEs en board?
        if len(master_grid.ups) != 0 or len(master_grid.crates) != 0:
            # Is there a safe path to UPs or CRATEs?
            if hero.safe_path_to_ups_or_crates(master_grid):
                return True
        # Is there a safe path to bot
        if hero.safe_path_to_bot(master_grid):
            return True
        else:
            # Find closest safe TILE
            hero.move_to_safety(master_grid.safety_map)
            return True

    # Methods related to CRATEs or UPs
    def next_to_a_crate(self, master_grid):
        isHeroNextCrate = False
    
        for k, crate in master_grid.crates.items():
            # Is there a crate next to HERO?
            if (math.fabs(self.x - crate.x) <= self.bomb_reach and self.y == crate.y) or (math.fabs(self.y - crate.y) <= self.bomb_reach and hero.x == crate.x):
                isHeroNextCrate = True
                break
        return isHeroNextCrate

    def safe_path_to_ups_or_crates(self,master_grid):
        ux, uy = None, None
        min_du = 5
        cx, cy = None, None
        min_dc = 5
        hasFoundSafeCrate = False
        hasFoundSafeUp = False
        if len(master_grid.ups) != 0:
            for k, up in master_grid.ups.items():
                dist, dx, dy = distance(self, up.x, up.y)

                # Arriving TILEs:
                north = (up.y-1 if up.y-1 > 0 else 0, up.x)
                south = (up.y+1 if up.y+1 < master_grid.height else 0, master_grid.height)
                east = (up.y,up.x+1 if up.x+1 < master_grid.width else master_grid.width)
                west = (up.y,up.x-1 if up.x-1 > 0 else 0)

                north_path = astar(master.safety_map, (self.y, self.x), north)
                south_path = astar(master.safety_map, (self.y, self.x), south)
                east_path =  astar(master.safety_map, (self.y, self.x), east)
                west_path = astar(master.safety_map, (self.y, self.x), west)

                if dist < min_du:
                    #XXX premier if non needed
                    if north_path or south_path  or  east_path or  west_path != False:
                        if north_path:
                            ux = north[1]
                            uy = north[0]
                            min_du = dist
                            hasFoundSafeUp = True
                        if south_path:
                            ux = south[1]
                            uy = south[0]
                            min_du = dist
                            hasFoundSafeUp = True
                        if east_path:
                            ux = east[1]
                            uy = east[0]
                            min_du = dist
                            hasFoundSafeUp = True
                        if west_path:
                            ux = west[1]
                            uy = west[0]
                            min_du = dist
                            hasFoundSafeUp = True
                    else:
                        continue
        if len(master_grid.crates) != 0:
            for k, crate in master_grid.crates.items():
                dist,dx, dy = distance(self, crate.x, crate.y)

                # Arriving TILEs:
                north = (crate.y-1 if crate.y-1 > 0 else 0, crate.x)
                south = (crate.y+1 if crate.y+1 < master_grid.height else 0, master_grid.height)
                east = (crate.y,crate.x+1 if crate.x+1 < master_grid.width else master_grid.width)
                west = (crate.y,crate.x-1 if crate.x-1 > 0 else 0)

                north_path = astar(master.safety_map, (self.y, self.x), north)
                south_path = astar(master.safety_map, (self.y, self.x), south)
                east_path =  astar(master.safety_map, (self.y, self.x), east)
                west_path = astar(master.safety_map, (self.y, self.x), west)

                if dist < min_dc:
                    if north_path or south_path  or  east_path or  west_path != False:
                        if north_path:
                            cx = north[1]
                            cy = north[0]
                            min_dc = dist
                            hasFoundSafeCrate = True
                        if south_path:
                            cx = south[1]
                            cy = south[0]
                            min_dc = dist
                            hasFoundSafeCrate = True
                        if east_path:
                            cx = east[1]
                            cy = east[0]
                            min_dc = dist
                            hasFoundSafeCrate = True
                        if west_path:
                            cx = west[1]
                            cy = west[0]
                            min_dc = dist
                            hasFoundSafeCrate = True
                    else:
                        continue

        if hasFoundSafeUp and hasFoundSafeCrate:
            if min_dc < min_du:
                self.DEST = [cx, cy]
                return True
            else:
                self.DEST = [ux, uy]
                return True
        elif hasFoundSafeUp or hasFoundSafeCrate:
            if hasFoundSafeUp:
                self.DEST = [ux, uy]
                return True
            else:
                self.DEST = [cx, cy]
                return True
        else:
            return False


    def safe_path_to_bot(self,master_grid):
        bx, by = None, None
        min_db = 1e5
        hasFoundSafeBot = False
        for k, bot in master_grid.bots.items():
            dist,dx, dy = distance(self, bot.x, bot.y)

            # Arriving TILEs:
            north = (bot.y-1 if bot.y-1 > 0 else 0, bot.x)
            south = (bot.y+1 if bot.y+1 < master_grid.height else 0, master_grid.height)
            east = (bot.y,bot.x+1 if bot.x+1 < master_grid.width else master_grid.width)
            west = (bot.y,bot.x-1 if bot.x-1 > 0 else 0)

            north_path = astar(master.safety_map, (self.y, self.x), north)
            south_path = astar(master.safety_map, (self.y, self.x), south)
            east_path =  astar(master.safety_map, (self.y, self.x), east)
            west_path = astar(master.safety_map, (self.y, self.x), west)

            if dist < min_db:
                if north_path or south_path  or  east_path or  west_path != False:
                    if north_path:
                        bx = north[1]
                        by = north[0]
                        min_db = dist
                        hasFoundSafeUp = True
                    if south_path:
                        bx = south[1]
                        by = south[0]
                        min_db = dist
                        hasFoundSafeUp = True
                    if east_path:
                        bx = east[1]
                        by = east[0]
                        min_db = dist
                        hasFoundSafeUp = True
                    if west_path:
                        bx = west[1]
                        by = west[0]
                        min_db = dist
                        hasFoundSafeUp = True
                else:
                    continue

        if hasFoundSafeBot:
            self.DEST = [bx, by]
            return True
        else:
            return False


    # Methods related to BOTS
    def next_to_a_bot(self, master_grid):
        isHeroNextBOT = False
    
        for k, bot in master_grid.bots.items():
            # Is there a bot next to HERO?
            if (math.fabs(self.x - bot.x) <= self.bomb_reach and self.y == bot.y) or (math.fabs(self.y - bot.y) <= self.bomb_reach and hero.x == bot.x):
                isHeroNextBOT = True
                break
        return isHeroNextBOT

    # Methods related to Bombs
    def move_to_safety(self, safety_map, isbomb=False):
        """Find closest safe tile

        """
        posx = 0
        posy = 0
        height, width = safety_map.shape
        mdist = height+width
        hasFoundSafeTile = False
        hx = self.next_move[1] if isbomb else self.x
        hy = self.next_move[0] if isbomb else self.y

        #XXX
        if isbomb:
            print("with bomb", file=sys.stderr)

        for i in range(height):
            for j in range(width):
                # distance of Tile(i,j) from Hero
                dist,dx, dy = distance(self, j, i)
                if safety_map[i, j] < safety_map[hy, hx] and dist < mdist:
                    # Find a safe path to tile
                    if astar(safety_map, (hy, hx), (i,j)) != False:
                        posx = j
                        posy = i
                        mdist = dist
                        hasFoundSafeTile = True
                    else:
                        # No safe path to Tile, find next safety Tile.
                        continue
        if hasFoundSafeTile:
            self.DEST = [posx, posy]
            return True
        else:
            # Add possibility of not finding a safe TILE.
            self.DEST = self.DEST
            #self.DEST = [random.randint(0,width), random.randint(0,height)]
            return False

    
    def safe_to_bomb(self,master_grid):
        # find next move to DEST
        # Arriving TILEs:
        north = (self.DEST[1]-1 if self.DEST[1]-1 > 0 else 0, self.DEST[0])
        south = (self.DEST[1]+1 if self.DEST[1]+1 < master_grid.height else 0, master_grid.height)
        east = (self.DEST[1],self.DEST[0]+1 if self.DEST[0]+1 < master_grid.width else master_grid.width)
        west = (self.DEST[1],self.DEST[0]-1 if self.DEST[0]-1 > 0 else 0)

        north_path = astar(master.safety_map, (self.y, self.x), north)
        south_path = astar(master.safety_map, (self.y, self.x), south)
        east_path =  astar(master.safety_map, (self.y, self.x), east)
        west_path = astar(master.safety_map, (self.y, self.x), west)

        #XXX
        print("paths", north_path, south_path, east_path, west_path, sep=" ", file=sys.stderr)
        

        if north_path != False and len(north_path) !=0 :
            self.next_move = north_path[::-1][0]
        if south_path != False and len(south_path) !=0 :
            self.next_move = south_path[::-1][0]
        if east_path != False and len(east_path) !=0 :
            self.next_move = east_path[::-1][0]
        if west_path != False and len(west_path) !=0 :
            self.next_move = west_path[::-1][0]

        simulated_safety_map = master_grid.simulate_safety_grid(self.x, self.y, self.bomb_reach)
        
        #XXX
        print("simu:", simulated_safety_map, file=sys.stderr)
        if hero.move_to_safety(simulated_safety_map, isbomb=True):
            return True
        else:
            return False


# Creating wall class
class Wall():
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Dictionary saving position of all Walls on the board
walls = {}
isWall = True
nwalls = 0

# Creating Class crate
class Crate:
    def __init__(self, x, y, crate_obj):
        self.x = x
        self.y = y
        self.obj = crate_obj


##### START GAME #####

# Set grid dimensions and HERO id
width, height, my_id = [int(i) for i in input().split()]

# Saving the grid in a matrix
grid = np.array([['.' for j in range(width)] for i in range(height)])
safety_map = np.array([[0 for j in range(width)] for i in range(height)])

master = MasterGrid(grid, safety_map)

# Creating hero entity
hero = Hero(entity_type=0, owner=my_id)

# game loop
while True:
    # Dictinary saving the crates
    crates_dict = {}
    ncrate = 0
    for i in range(height):
        row = input()
        # Populating the grid
        for j in range(width):
            master.grid[i,j] = row[j]
            # Populating the Crates
            if row[j] != '.' and row[j] != 'X':
                crates_dict[ncrate] = Crate(j, i, row[j])
                ncrate += 1
            if isWall:
                # Populating the Walls
                if row[j] == 'X':
                    walls[nwalls] = Wall(j,i)
                    nwalls += 1

    # Setting Wall flag to False so we do not populate the dict next turn (wall
    # position won't move)
    isWall = False
                
    isHeroOnABomb = False

    # Dictionaries saving each entity types
    all_bombs = {}
    bots = {}
    obj_ups = {}
    nb_bombs = 0
    nups = 0
    nbots = 0
    # Entities
    entities = int(input())

    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        # Populating each entity dictionaries
        if entity_type == 0:
            if owner == my_id:
                if isFirstTurn:
                    hero.x = x
                    hero.y = y
                    hero.DEST[0] = x
                    hero.DEST[1] = y
                    isFirstTurn = False
                else:
                    hero.past_x = hero.x
                    hero.past_y = hero.y
                    hero.x = x
                    hero.y = y
                hero.param_1 = param_1
                hero.param_2 = param_2
            else:
                bots[nbots] = Entity(entity_type, owner, x, y, param_1, param_2)
                nbots += 1
        elif entity_type == 1:
            if owner == my_id:
                all_bombs[nb_bombs] = Entity(entity_type, owner, x, y, param_1, param_2)
                nb_bombs += 1
            if hero.x == x and hero.y == y:
                isHeroOnABomb = True
            if owner == my_id:
                hero.bomb_reach = param_2
        elif entity_type == 2:
            if owner == my_id:
                obj_ups[nups] = Entity(entity_type, owner, x, y, param_1, param_2)
                nups += 1
        else:
            print("Wrong type of entity", file=sys.stderr)

    # Populating the crates with near bomb dictionary
    crates_bombs = {}
    nb_crate_bomb = 0
    for k, crate in crates_dict.items():
        for k, bomb in all_bombs.items():
            if math.fabs(bomb.x-crate.x) == 1 or math.fabs(bomb.y-crate.y) == 1:
                crates_bombs[nb_crate_bomb] = [crate.x, crate.y]

    master.all_bombs= all_bombs
    master.bots = bots
    master.ups = obj_ups
    master.crates = crates_dict

    
    # Populating the safety_map
    master.init_safety_map()

    ## DEBUG Algo working
    #print(master.safety_map, file=sys.stderr)

    '''
    ##### HERO Actions #####
        -- is HERO safe?
            yes -- is HERO near crate or bot?
                yes -- has HERO reach DEST?
                    yes -- find new DEST    --> BOMB Dx Dy
                    no  -- BOMB Dx Dy
                no  -- has HERO reach DEST?
                    yes -- find new DEST    --> MOVE Dx Dy
                    no  -- MOVE Dx Dy
            no  -- find closest save TILE   --> MOVE Tx Ty

    ##### HERO find DEST #####
        -- is there UPs on board?
            yes -- find safest path to UPs  --> MOVE Ux Uy
            no  -- is there crate on board?
                yes -- find safest path to crate    --> MOVE Cx Cy
                no  -- for each BOT on board <find safest and shorter path to BOT>  --> MOVE Bx By
    '''
    
    if master.safety_map[hero.y, hero.x] > 8:
        hero.move_to_safety(master.safety_map)
        print("MOVE", hero.DEST[0],hero.DEST[1], "DANGER!", sep=" ")
    else:
        isHeroNearBot = hero.next_to_a_bot(master)
        isHeroNearCrate = hero.next_to_a_crate(master)
        if isHeroNearBot or isHeroNearCrate:
            if hero.has_reach_destination():
                hero.find_new_destination(master)
            if  hero.param_1 != 0 and hero.safe_to_bomb(master):
                print("BOMB", hero.DEST[0], hero.DEST[1])
            else:
                print("MOVE", hero.DEST[0], hero.DEST[1])

        else:
            if hero.has_reach_destination():
                hero.find_new_destination(master)

            print("MOVE", hero.DEST[0], hero.DEST[1])




