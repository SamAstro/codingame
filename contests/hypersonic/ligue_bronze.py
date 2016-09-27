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
    dx = math.fabs(cx - hero.x)
    dy = math.fabs(cy - hero.y)
    dist = dx + dy

    return dist

def find_closest_safe_up(hero, master):
    dmin = 10
    posx = 0
    posy = 0
    for k,up in master.ups.items():
        dist = distance(hero, up.x, up.y)
        if dist < dmin:
            print("UPs", astar(safety_map, (hero.y, hero.x), (up.y, up.x)),sep=" ", file=sys.stderr)
            if astar(master.safety_map, (hero.y, hero.x), (up.y, up.x)) != False:
                posx = up.x
                posy = up.y
                dmin = dist
            else:
                continue
    print("MOVE", posx, posy, sep=" ")
    hero.DEST = [posx, posy]

def find_closest_safe_crate(hero, master):
    dmin = 3
    posx = 0
    hasFoundCrate = False
    posy = 0
    for k,crate in master.crates.items():
        dist = distance(hero, crate.x, crate.y)
        if dist < dmin:
            dir_x = 0
            dir_y = 0
            if hero.x == crate.x:
                if hero.y < crate.y:
                    dir_y = -1
                else:
                    dir_y = +1
           
            if hero.y == crate.y:
                if hero.x < crate.x:
                    dir_x = -1
                else:
                    dir_x = +1
            if astar(master.safety_map, (hero.y, hero.x), (crate.y+dir_y, crate.x+dir_x)) != False:
                posx = crate.x
                posy = crate.y
                dmin = dist
                hasFoundCrate = True
            else:
                continue
    return hasFoundCrate, posx, posy

def find_bot_onboard(hero, bots):
    posx, posy = 0,0
    isBotNear = False
    for k, bot in bots.items():
        dist = distance(hero, bot.x, bot.y)
        if (hero.y == bot.y and dist < hero.bomb_reach) or (hero.x and bot.x and dist< hero.bomb_reach):
            isBotNear = True
            posx = bot.x
            posy = bot.y
    return isBotNear, posx, posy

##### CLASSES #####

class MasterGrid():
    def __init__(self, grid, safety_map, crates = {}, all_bombs = {}, ups={}):
        height,width = grid.shape
        self.width = width
        self.height = height
        self.grid = grid
        self.safety_map = safety_map
        self.crates = crates
        self.all_bombs = all_bombs
        self.ups = ups

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
                            self.safety_map[i,start:end] = 9 - delta
        for i in range(self.height):
            for j in range(self.width):
                # Setting back walls and crates to danger of 8
                if self.grid[i,j] != ".":
                    self.safety_map[i,j] = -1


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
    hasReachDEST = False

    def __init__(self, entity_type=0, owner=0, x=0, y=0, param_1=0, param_2=0):
        super().__init__(entity_type=0, owner=0, x=0, y=0, param_1=0, param_2=0)

    # Methods related to DESTINATION
    def has_reach_destination(self):
        if hero.x == hero.DEST[0] and hero.y == hero.DEST[1]:
            print("hello!", file=sys.stderr)
            hero.hasReachDEST = True
            return True
        else:
            hero.hasReachDEST = False
            return False

    def find_new_destination(self, master_grid):
        if len(master_grid.ups) != 0:
            print("UPPPPSsss", file=sys.stderr)
            # find shorter and safer path to closest UPs
            find_closest_safe_up(self, master_grid)
        else:
            isHeroNextCrate, posx_crate, posy_crate = find_closest_safe_crate(self, master_grid)
            print("Crate... ?", file=sys.stderr)
            if isHeroNextCrate:
                print("...YES!", file=sys.stderr)
                print("MOVE", posx_crate, posy_crate)
                hero.DEST = [posx_crate, posy_crate]
            else:
                print("...NO!", file=sys.stderr)
                isBotNear, posx_bot, posy_bot = find_bot_onboard(hero,bots)
                print("BOT...?", file=sys.stderr)
                if isBotNear:
                    print("...Yes!", file=sys.stderr)
                    print("MOVE", posx_bot, posy_bot)
                    hero.DEST = [posx_bot, posy_bot]
                else:
                    print("MOVE", random.randint(0,width), random.randint(0,height), sep=" ")

    # Methods related to crates
    def move_to_crate(self, posx, posy):
        print("MOVE", posx, posy, sep=" ")

    def bomb_crate(self, posx, posy):
        print("BOMB", posx, posy, sep=" ")

    def next_to_a_crate(self, safety_map, crates, crates_bombs):
        print("Am I near a crate?", file=sys.stderr)
        isHeroNextCrate = False
        posx_crate, posy_crate = None, None
    
        for k, crate in crates.items():
            # Is there a crate next to HERO?
            if (math.fabs(hero.x - crate.x) < 3 and hero.y == crate.y) or (math.fabs(hero.y - crate.y) < 3 and hero.x == crate.x):
                print("YES I AM!!", file=sys.stderr)
                isHeroNextCrate = True
                posx_crate, posy_crate = crate.x, crate.y
                break

        return isHeroNextCrate, posx_crate, posy_crate

    # Methods related to Bombs
    def bomb_under(self, bombs):
        isBombUnderHero = False
        
        for k, bomb in bombs.items():
            if (hero.x == bomb.x and hero.y == bomb.y):
                isBombUnderHero = True
                break
        return isBombUnderHero

    # Methods related to Ups
    def move_to_ups(self, posx, posy):
        print("MOVE", posx, posy, sep=" ")

    # Methods related to Enemy Bombs
    def move_to_safety(self, safety_map):
        """Find closest safe tile

        """
        posx = 0
        posy = 0
        height, width = safety_map.shape
        mdist = height+width

        for i in range(height):
            for j in range(width):
                # distance of Tile(i,j) from Hero
                dist = distance(self, j, i)
                if safety_map[i, j] == 0 and dist < mdist:
                    # Find a safe path to tile
                    print("TILE", astar(safety_map, (hero.y, hero.x), (i,j)), sep=" ", file=sys.stderr)
                    if astar(safety_map, (hero.y, hero.x), (i,j)) != False:
                        posx = j
                        posy = i
                        mdist = dist
                    else:
                        # No safe path to Tile, find next safety Tile.
                        continue
        print("MOVE", posx, posy, sep=" ")
        self.DEST = [posx, posy]



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
            all_bombs[nb_bombs] = Entity(entity_type, owner, x, y, param_1, param_2)
            nb_bombs += 1
            if hero.x == x and hero.y == y:
                isHeroOnABomb = True
            if owner == my_id:
                hero.bomb_reach = param_2-1
        elif entity_type == 2:
            obj_ups[nups] = Entity(entity_type, owner, x, y, param_1, param_2)
            nups += 1
        else:
            print("Wrong type of entity")

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
    #print(astar(master.safety_map, (10,12), (10,11)), file=sys.stderr)


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
    
    if master.safety_map[hero.y, hero.x] != 0:
        hero.move_to_safety(master.safety_map)
        print("HERO DANGER", file=sys.stderr)
    else:
        isBotNear, posx_bot, posy_bot = find_bot_onboard(hero,bots)
        isHeroNextCrate, posx_crate, posy_crate = hero.next_to_a_crate(master.safety_map, crates_dict, crates_bombs)
        if isBotNear or isHeroNextCrate:
            print("bot or crate", file=sys.stderr)
            if hero.has_reach_destination():
                hero.find_new_destination(master)
            else:
                print("BOMB", hero.DEST[0], hero.DEST[1])
        else:
            if hero.has_reach_destination():
                hero.find_new_destination(master)
            else:
                print("MOVE", hero.DEST[0], hero.DEST[1])
