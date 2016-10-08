import sys
import math
import numpy as np
import random

# Flags
isFirstTurn = True
isDEBUG = False

# Reproducing randomness -- FOR DEBUG ONLY
#random.seed(9001)


#NOTES Add awareness of crates or walls blocking bomb explosion

# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

import numpy
from heapq import *


# Manhattan distance: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#S7
#function heuristic(node) =
#    dx = abs(node.x - goal.x)
#    dy = abs(node.y - goal.y)
#    return D * (dx + dy)



def heuristic(a, b):
    return math.fabs(a[0] - b[0]) + math.fabs(a[1] - b[1])
    #return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
    #neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

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
    dx = cx - hero.x
    dy = cy - hero.y
    dist = math.fabs(dx) + math.fabs(dy)

    return dist

def distance2(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
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
                        # Setting maximal range of explosion horizontally
                        start = j-bomb.param_2 if  j-bomb.param_2 > 0 else 0
                        end =  j+bomb.param_2 if  j+bomb.param_2 < width else width-1

                        mldist = 13
                        mldx = 13
                        block_left = (None, None)
                        mrdist = 13
                        mrdx = 13
                        block_right = (None, None)

                        # Scanning for blocking block on the x-axis
                        ## On the left of the bomb
                        for jj in range(start, j):
                            # Find closest blocking block:
                                ldx = jj - j
                                ldist = math.fabs(ldx)
                                if ldist < mldist and self.grid[i, jj] != '.':
                                    mldist = ldist
                                    mldx = ldx
                                    block_left = (jj, i)

                        ## On the right of the bomb
                        for jj in range(j, end):
                            # Find closest blocking block:
                                rdx = jj - j
                                rdist = math.fabs(rdx)
                                if rdist < mrdist and self.grid[i, jj] != '.':
                                    mrdist = rdist
                                    mrdx = rdx
                                    block_right = (jj,i)

                        ## Setting row Tiles between block_left and block_right to danger
                        start_block = block_left[0] if block_left[0] != None else start
                        end_block = block_right[0] if block_right[0] != None else end

                        for jj in range (start_block, end_block):
                            delta = math.fabs(j-jj)
                            self.safety_map[i,jj] = 9 - delta if delta != 9 else 1


                        # Setting maximal range of explosion vertically
                        start = i-bomb.param_2 if  i-bomb.param_2 > 0 else 0
                        end =  i+bomb.param_2 if  i+bomb.param_2 < height else height -1

                        mtdist = 13
                        mtdx = 13
                        block_top = (None, None)
                        mddist = 13
                        mddx = 13
                        block_down = (None, None)

                        # Scanning for blocking block on the y-axis
                        ## On the top of the bomb
                        for ii in range(start, i):
                            # Find closest blocking block:
                                tdx = ii - i
                                tdist = math.fabs(tdx)
                                if tdist < mtdist and self.grid[ii, j] != '.':
                                    mtdist = tdist
                                    mtdx = tdx
                                    block_top = (j, ii)

                        ## On the right of the bomb
                        for ii in range(i, end):
                            # Find closest blocking block:
                                ddx = ii-i
                                ddist = math.fabs(ddx)
                                if ddist < mddist and self.grid[ii, j] != '.':
                                    mddist = ddist
                                    mddx = ddx
                                    block_down = (j,ii)

                        ## Setting row Tiles between block_left and block_right to danger
                        start_block = block_top[1] if block_top[1] != None else start
                        end_block = block_down[1] if block_down[1] != None else end

                        for ii in range (start_block, end_block):
                            delta = math.fabs(i-ii)
                            self.safety_map[ii,j] = 9 - delta if delta != 9 else 1


        # Setting back walls and crates to -1
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i,j] != ".":
                    self.safety_map[i,j] = -1

    def simulate_safety_grid(self, bx, by, bomb_reach):
        #XXX
        if isDEBUG:
            print("Simulating the safety grid -- bomb @", bx, by, sep=" ", file=sys.stderr)
        self.simulated_safety_map = np.copy(self.safety_map)

       
        # Setting maximal range of explosion
        start = bx-bomb_reach if  bx-bomb_reach > 0 else 0
        end =  bx+bomb_reach+1 if  bx+bomb_reach+1 < width else width

        mldist = 13
        mldx = 13
        block_left = (None, None)
        mrdist = 13
        mrdx = 13
        block_right = (None, None)

        # Scanning for blocking block on the x-axis
        ## On the left of the bomb
        for j in range(start, bx):
            # Find closest blocking block:
                ldx = j - bx
                ldist = math.fabs(ldx)
                if ldist < mldist and self.grid[by, j] != '.':
                    mldist = ldist
                    mldx = ldx
                    block_left = (j, by)

        ## On the right of the bomb
        for j in range(bx, end):
            # Find closest blocking block:
                rdx = j - bx
                rdist = math.fabs(rdx)
                if rdist < mrdist and self.grid[by, j] != '.':
                    mrdist = rdist
                    mrdx = rdx
                    block_right = (j, by)

        ## Setting row Tiles between block_left and block_right to danger
        start_block = block_left[0] if block_left[0] != None else start
        end_block = block_right[0] if block_right[0] != None else end

        for j in range (start_block, end_block):
            delta = math.fabs(bx-j)
            self.simulated_safety_map[by,j] = 9 - delta if delta != 9 else 1



        # Setting maximal range of explosion
        start = by-bomb_reach if  by-bomb_reach > 0 else 0
        end =  by+bomb_reach+1 if  by+bomb_reach+1 < height else height

        mtdist = 13
        mtdx = 13
        block_top = (None, None)
        mddist = 13
        mddx = 13
        block_down = (None, None)

        # Scanning for blocking block on the y-axis
        ## On the left of the bomb
        for i in range(start, by):
            # Find closest blocking block:
                tdx = i - by
                tdist = math.fabs(tdx)
                if tdist < mtdist and self.grid[i, bx] != '.':
                    mtdist = tdist
                    mtdx = tdx
                    block_top = (bx, i)

        ## On the down of the bomb
        for i in range(by, end):
            # Find closest blocking block:
                ddx = i - by
                ddist = math.fabs(ddx)
                if ddist < mddist and self.grid[i, bx] != '.':
                    mddist = ddist
                    mddx = ddx
                    block_down = (bx, i)

        ## Setting column Tiles between block_top and block_down to danger
        start_block = block_top[1] if block_top[1] != None else start
        end_block = block_down[1] if block_down[1] != None else end

        for i in range (start_block, end_block):
            delta = math.fabs(by-i)
            self.simulated_safety_map[i,bx] = 9 - delta if delta != 9 else 1


        for i in range(self.height):
            for j in range(self.width):
                # Setting back walls and crates to -1
                if self.grid[i,j] != ".":
                    self.simulated_safety_map[i,j] = -1

        return self.simulated_safety_map


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
    ticking_bomb = 7
    max_bomb = 1


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
    def at_intersection(self, master_grid, intersection_row, intersection_column):
        isHeroAtInter = False
    
        for k, crate in master_grid.crates.items():
            # Is there a crate next to HERO?
            dist = distance(self, crate.x, crate.y)
            if (crate.x in intersection_row or crate.y in intersection_column) and (self.x in intersection_row and self.y in intersection_column) and dist < self.bomb_reach:
                isHeroAtInter = True
                break
        return isHeroAtInter

    def next_to_a_crate(self, master_grid):
        isHeroNextCrate = False
    
        for k, crate in master_grid.crates.items():
            # Is there a crate next to HERO?
            if (math.fabs(self.x - crate.x) <= 1 and self.y == crate.y) or (math.fabs(self.y - crate.y) <= 1 and hero.x == crate.x):
            #if (math.fabs(self.x - crate.x) <= self.bomb_reach and self.y == crate.y) or (math.fabs(self.y - crate.y) <= self.bomb_reach and hero.x == crate.x):
                isHeroNextCrate = True
                break
        return isHeroNextCrate

    def next_to_a_up(self, master_grid):
        isHeroNextUP = False
        ux, uy = None, None
    
        for k, up in master_grid.ups.items():
            dist = distance(self, up.x, up.y)

            # Is there a crate next to HERO?
            if dist <=4:
            #if (math.fabs(self.x - crate.x) <= self.bomb_reach and self.y == crate.y) or (math.fabs(self.y - crate.y) <= self.bomb_reach and hero.x == crate.x):
                isHeroNextUP = True
                ux = up.x
                uy = up.y
                break
        return isHeroNextUP, ux, uy

    def safe_path_to_ups_or_crates(self,master_grid):
        ux, uy = None, None
        min_du = 24
        cx, cy = None, None
        min_dc = 24
        hasFoundSafeCrate = False
        hasFoundSafeUp = False
        safety_nb_saved = 0

        if len(master_grid.ups) != 0:
            for k, up in master_grid.ups.items():
                dist = distance(self, up.x, up.y)

                if dist < min_du:
                    # Setting ARRIVAL TILE safety to 0
                    safety_nb_saved = master.safety_map[up.y, up.x]
                    master.safety_map[up.y, up.x] = 0

                    safe_path = astar(master.safety_map, (self.y, self.x), (up.y, up.x))

                    if safe_path != False and len(safe_path) != 0:
                        self.next_move = safe_path[::-1][1] if len(safe_path) != 1 else safe_path[::-1][0]
                        ux = up.x
                        uy = up.y
                        min_du = dist
                        hasFoundSafeUp = True
                    else:
                        continue

                    # Putting value back
                    master.safety_map[up.y, up.x] = safety_nb_saved


        if len(master_grid.crates) != 0:
            for k, crate in master_grid.crates.items():
                dist = distance(self, crate.x, crate.y)

                if dist < min_dc:
                    # Setting ARRIVAL TILE safety to 0
                    safety_nb_saved = master.safety_map[crate.y, crate.x]
                    master.safety_map[crate.y, crate.x] = 0

                    safe_path = astar(master.safety_map, (self.y, self.x), (crate.y, crate.x))

                    if safe_path != False and len(safe_path) != 0:
                        self.next_move = safe_path[::-1][1] if len(safe_path) != 1 else safe_path[::-1][0]
                        cx = crate.x
                        cy = crate.y
                        min_dc = dist
                        hasFoundSafeCrate = True

                    else:
                        continue

                    # Putting value back
                    master.safety_map[crate.y, crate.x] = safety_nb_saved

        if hasFoundSafeCrate:
            self.DEST = [cx, cy]
            return True
        elif hasFoundSafeUp:
            self.DEST = [ux, uy]
            return True
        else:
            return False


        #if hasFoundSafeUp and hasFoundSafeCrate:
        #    if min_dc < min_du:
        #        self.DEST = [cx, cy]
        #        return True
        #    else:
        #        self.DEST = [ux, uy]
        #        return True
        #elif hasFoundSafeUp or hasFoundSafeCrate:
        #    if hasFoundSafeUp:
        #        self.DEST = [ux, uy]
        #        return True
        #    else:
        #        self.DEST = [cx, cy]
        #        return True
        #else:
        #    return False


    def safe_path_to_bot(self,master_grid):
        bx, by = None, None
        min_db = 1e5
        hasFoundSafeBot = False
        if self.x == bx and self.y == by:
            return False
        else:
            for k, bot in master_grid.bots.items():
                dist = distance(self, bot.x, bot.y)

                if dist < min_db:
                    # Setting ARRIVAL TILE safety to 0
                    safety_nb_saved = master.safety_map[bot.y, bot.x]
                    master.safety_map[bot.y, bot.x] = 0

                    safe_path = astar(master.safety_map, (self.y, self.x), (bot.y, bot.x))

                    if safe_path != False and len(safe_path) != 0:
                        self.next_move = safe_path[::-1][1] if len(safe_path) != 1 else safe_path[::-1][0]
                        bx = bot.x
                        by = bot.y
                        min_db = dist
                        hasFoundSafeBot = True
                    else:
                        continue

                    # Putting value back
                    master.safety_map[bot.y, bot.x] = safety_nb_saved

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
            if (math.fabs(self.x - bot.x) <= 1 and self.y == bot.y) or (math.fabs(self.y - bot.y) <= 1 and hero.x == bot.x):
            #if (math.fabs(self.x - bot.x) <= self.bomb_reach and self.y == bot.y) or (math.fabs(self.y - bot.y) <= self.bomb_reach and hero.x == bot.x):
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
        hx = self.x
        hy = self.y

        for i in range(height):
            for j in range(width):
                # distance of Tile(i,j) from Hero
                dist = distance(self, j, i)
                if safety_map[i, j] == 0 and dist < mdist:
                #if safety_map[i, j] < safety_map[hy, hx] and dist < mdist:
                    # Find a safe path to tile
                    safe_path = astar(safety_map, (hy, hx), (i,j))
                    if safe_path != False and len(safe_path) <= self.ticking_bomb:
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

        # Setting ARRIVAL TILE safety to 0
        safety_nb_saved = master.safety_map[self.DEST[1], self.DEST[0]]
        master.safety_map[self.DEST[1], self.DEST[0]] = 0

        safe_path = astar(master.safety_map, (self.y, self.x), (self.DEST[1], self.DEST[0]))

        master.safety_map[self.DEST[1], self.DEST[0]] = safety_nb_saved

        if safe_path != False  and len(safe_path) != 0:
            self.next_move = safe_path[::-1][1] if len(safe_path) != 1 else safe_path[::-1][0]


        simulated_safety_map = master_grid.simulate_safety_grid(self.x, self.y, self.bomb_reach)

        #XXX
        if isDEBUG:
            print("simu", simulated_safety_map,file=sys.stderr)
        
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
voisins = [(0,1),(0,-1),(1,0),(-1,0)]

# Creating hero entity
hero = Hero(entity_type=0, owner=my_id)
hero.max_bomb = 1
intersection_row = np.array([j for j in range(0, width, 2)])
intersection_column = np.array([i for i in range(0, height, 2)])

# game loop
while True:
    hero.ticking_bomb = 7
    # Dictinary saving the crates
    voisin = []
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
                if param_1 > hero.max_bomb:
                    hero.max_bomb = param_1
            else:
                bots[nbots] = Entity(entity_type, owner, x, y, param_1, param_2)
                nbots += 1
        elif entity_type == 1:
            all_bombs[nb_bombs] = Entity(entity_type, owner, x, y, param_1, param_2)
            if param_1 < hero.ticking_bomb:
                hero.ticking_bomb = param_1 -1
            nb_bombs += 1
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
    #XXX
    if isDEBUG:
        print(master.safety_map, file=sys.stderr)

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

    if len(master.crates) == 0:
        for i,j in voisins:
                voisin.append((hero.DEST[0]+i, hero.DEST[1] + j))


        if hero.param_1 == hero.max_bomb:
            print("1ere bombe", file=sys.stderr)
            hero.DEST[0] = master.bots[0].x - 1 if master.bots[0].x > 0 else master.bots[0].x + 1
            hero.DEST[1] = master.bots[0].y - 2 if master.bots[0].y > 2 else master.bots[0].y +2

            if hero.has_reach_destination():
                hero.DEST[0] = master.bots[0].x + 1 if master.bots[0].x > 0 else master.bots[0].x - 1
                hero.DEST[1] = master.bots[0].y - 2 if master.bots[0].y > 2 else master.bots[0].y +2

                print("BOMB", hero.DEST[0], hero.DEST[1], sep=" ")
            else:
                print("MOVE", hero.DEST[0], hero.DEST[1], sep=" ")

        elif hero.param_1 == hero.max_bomb-1:
            print("2eme bombe", file=sys.stderr)
            if hero.has_reach_destination():
                hero.DEST[0] = master.bots[0].x + 1 if master.bots[0].x < width else master.bots[0].x - 1
                hero.DEST[1] = master.bots[0].y
                print("BOMB", hero.DEST[0], hero.DEST[1], sep=" ")
            else:
                print("MOVE", hero.DEST[0], hero.DEST[1], sep=" ")
        elif hero.param_1 == hero.max_bomb-2:
            print("3eme bombe", file=sys.stderr)
            if hero.has_reach_destination():
                hero.DEST[0] = master.bots[0].x
                hero.DEST[1] = master.bots[0].y +2 if master.bots[0].y < height-2 else height-1
                print("BOMB", hero.DEST[0], hero.DEST[1], sep=" ")
            else:
                print("MOVE", hero.DEST[0], hero.DEST[1], sep=" ")
        else:
            print("4ere bombe", file=sys.stderr)
            if hero.has_reach_destination():
                print("MOVE", hero.x, hero.y, sep=" ")
            else:
                print("MOVE", hero.DEST[0], hero.DEST[1], sep=" ")

    elif master.safety_map[hero.y, hero.x] == 0 and hero.ticking_bomb < 2:
        print("MOVE", hero.x,hero.y, "STAY PUT!", sep=" ")
    elif master.safety_map[hero.y, hero.x] != 0:# and ticking_bomb < 6:
        hero.move_to_safety(master.safety_map)
        print("MOVE", hero.DEST[0],hero.DEST[1], "DANGER!", sep=" ")
    else:
        isHeroNearBot = hero.next_to_a_bot(master)
        isHeroNearCrate = hero.next_to_a_crate(master)
        isHeroNearUp, ux, uy = hero.next_to_a_up(master)
        isHeroAtInter = hero.at_intersection(master, intersection_row, intersection_column)
 
        if len(master.crates) <= 5:
            # Mode kamikaze

            startx = master.bots[0].x - 3 if master.bots[0].x - 3 > 0 else 0
            endx = master.bots[0].x + 3 if master.bots[0].x + 3 < width-1 else width-1

            starty = master.bots[0].y - 3 if master.bots[0].y - 3 > 0 else 0
            endy = master.bots[0].y + 3 if master.bots[0].y + 3 < height-1 else height-1


            hx = random.randint(startx,endx)
            hy = random.randint(starty, endy)

            while master.safety_map[hy, hx] != 0:
                hx = random.randint(startx,endx)
                hy = random.randint(starty, endy)

            if hero.x in intersection_row and hero.y in intersection_column:
                print("MOVE", hx, hy)
                #print("BOMB", hx, hy)
            else:
                print("MOVE", hx, hy)

        elif isHeroNearUp:
            print("MOVE", ux, uy, sep=" ")

        elif isHeroNearBot or isHeroNearCrate or isHeroAtInter:
            for i,j in voisins:
                voisin.append((hero.DEST[0]+i, hero.DEST[1] + j))

            if (hero.x, hero.y) in voisin:
                #XXX
                if isDEBUG:
                    print("close to destination", file=sys.stderr)
                hero.DEST[0] = hero.x
                hero.DEST[1] = hero.y

            if hero.has_reach_destination():
                hero.find_new_destination(master)
            
            if  hero.param_1 != 0 and hero.safe_to_bomb(master):
                print("BOMB", hero.DEST[0], hero.DEST[1])
            elif master.safety_map[hero.next_move[0], hero.next_move[1]] <= master.safety_map[hero.y, hero.x] and hero.ticking_bomb > 1:
               print("MOVE", hero.DEST[0], hero.DEST[1])
            else:
                print("staying put!",hero.x, hero.y, sep=" ", file=sys.stderr)
                print("MOVE", hero.x, hero.y)

        else:
            if hero.has_reach_destination():
                hero.find_new_destination(master)

            if master.safety_map[hero.next_move[0], hero.next_move[1]] <= master.safety_map[hero.y, hero.x] and hero.ticking_bomb > 1:
               print("MOVE", hero.DEST[0], hero.DEST[1])
            else:
                print("staying put!",hero.x, hero.y, sep=" ", file=sys.stderr)
                print("MOVE", hero.x, hero.y)

