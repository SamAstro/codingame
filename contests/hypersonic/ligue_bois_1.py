#!/opt/local/bin/python
"""
BOT FOR THE 'LIGUE BOIS 1' OF THE 'HYPERSONIC' CONTEST

Version:    1.1
Created:    09/25/2016
Compiler:   python3.5

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Notes: 
"""
import sys
import math
import numpy as np
import random

# Flags
isHeroInDanger = False
isUpClose = False
isFirstTurn = True


##### FUNCTIONS #####
def distance(hero, cx, cy):
    distx = math.sqrt((cx - hero.x)**2)
    disty = math.sqrt((cy - hero.y)**2)
    return distx, disty

def find_random_crate(crates, crates_bombs):
    posx, posy = 0, 0
    isCrateFound = False

    if len(crates) == 0:
        isCrateFound = True
    
    while not isCrateFound:
        # Choose randomly a crate to bomb
        crate = crates[random.choice(list(crates.keys()))]
        isCrateBomb = False
        for k, crate_bomb in crates_bombs.items():
            if crate.x == crate_bomb[0] and crate.y == crate_bomb[1]:
                    isCrateBomb = True
                    break
                    
        if isCrateBomb:
            continue
        else:
            isCrateFound = True
            posx = crate.x
            posy = crate.y
                
    return posx, posy

def find_farest_crate(hero, crates, crates_bombs):
    posx, posy = 0, 0
    mdist = 0
    for k, crate in crates.items():
        # Is the crate already have a bomb next to it?
        isCrateBomb = False
        for kk, crate_bomb in crates_bombs.items():
            if crate.x == crate_bomb[0] and crate.y == crate_bomb[1]:
                isCrateBomb = True
                break

        if isCrateBomb:
            continue
        else:
            dx, dy = distance(hero, crate.x, crate.y)
            dist = math.sqrt(dx**2 + dy**2)
            if dist > mdist:
                posx = crate.x
                posy = crate.y
                mdist = dist
    return posx, posy

def find_closest_crate(hero, crates, crates_bombs):
    posx, posy = 0, 0
    mdist = 1.e5
    for k, crate in crates.items():
        # Is the crate already have a bomb next to it?
        isCrateBomb = False
        for kk, crate_bomb in crates_bombs.items():
            if crate.x == crate_bomb[0] and crate.y == crate_bomb[1]:
                isCrateBomb = True
                break

        if isCrateBomb:
            continue
        else:
            dx, dy = distance(hero, crate.x, crate.y)
            dist = math.sqrt(dx**2 + dy**2)
            if dist < mdist:
                posx = crate.x
                posy = crate.y
                mdist = dist
    return posx, posy


def find_ups_onboard(hero, obj_ups):
    dmin = 10
    posx = 0
    posy = 0
    isUpClose = False
    for k,ups in obj_ups.items():
        dx = hero.x - ups.x
        dy = hero.y - ups.y
        if math.sqrt(dx*dx + dy*dy) < dmin:
            posx = ups.x
            posy = ups.y
            dmin = math.sqrt(dx*dx + dy*dy)
            isUpClose = True
    return isUpClose, posx, posy


def find_bombs_onboard(hero, enemy_bombs):
    ebomb_range = None
    posx, posy = 0,0
    isHeroInDanger = False
    for k,bomb in enemy_bombs.items():
        ebomb_range = bomb.param_2 - 1
        ebomb_timer = bomb.param_1
        ebomb_constraint = 2 #max(ebomb_range, ebomb_timer)
        dx = hero.x - bomb.x
        dy = hero.y - bomb.y
        if (math.fabs(dx) < ebomb_constraint and dy == 0) or (math.fabs(dy) < ebomb_constraint and dx == 0):
            isHeroInDanger = True
            posx = bomb.x
            posy = bomb.y
    return isHeroInDanger, posx, posy, ebomb_range



##### CLASSES #####

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
    bomb_previous_turn = False

    def __init__(self, entity_type=0, owner=0, x=0, y=0, param_1=0, param_2=0):
        super().__init__(entity_type=0, owner=0, x=0, y=0, param_1=0, param_2=0)

    # Methods related to crates
    def move_to_crate(self, posx, posy):
        print("MOVE", posx, posy, sep=" ")

    def bomb_crate(self, posx, posy):
        print("BOMB", posx, posy, sep=" ")

    def next_to_a_crate(self, crates, crates_bombs):
        isHeroNextCrate = False
        posx_crate, posy_crate = None, None
    
        for k, crate in crates.items():
            # Is there a crate next to HERO?
            if (math.fabs(hero.x - crate.x) == 1 and hero.y == crate.y) or (math.fabs(hero.y - crate.y) == 1 and hero.x == crate.x):
                print("HERO next to crate... can we bomb?", file=sys.stderr)
                #Is there already a bomb with the crate?
                isCrateBomb = False
                for kk, crate_bomb in crates_bombs.items():
                    if crate.x == crate_bomb[0] and crate.y == crate_bomb[1]:
                        isCrateBomb = True
                        break

                if isCrateBomb:
                    continue
                else:
                    isHeroNextCrate = True
                    posx_crate, posy_crate = crate.x, crate.y
                    hero.bomb_previous_turn = True
                    break

        return isHeroNextCrate, posx_crate, posy_crate

    # Methods related to Bombs
    def bomb_under(self, enemy_bombs, hero_bombs):
        isBombUnderHero = False
        
        for k, ebomb in enemy_bombs.items():
            if (hero.x == ebomb.x and hero.y == ebomb.y):
                isBombUnderHero = True
                break

        if not isBombUnderHero:
            for k, hbomb in hero_bombs.items():
                if (hero.x == hbomb.x and hero.y == hbomb.y):
                    isBombUnderHero = True
                    break

        return isBombUnderHero

    # Methods related to Ups
    def move_to_ups(self, posx, posy):
        print("MOVE", posx, posy, sep=" ")

    # Methods related to Enemy Bombs
    def move_away_from_bombs(self, posx_bomb, posy_bomb, grid, ebomb_reach=2):
        posx = 0
        posy = 0

        deplx = 1 if self.x + 1 < width - 1 else -1
        deply = 1 if self.y + 1 < height - 1 else -1


        dx = self.x - posx_bomb
        dy = self.y - posy_bomb
        
        deltax = -deplx if self.x -deplx > 0 else deplx
        deltay = -deply if self.y -deply > 0 else deply

        if math.fabs(dx)<ebomb_reach:
            posx = self.x
            if grid[self.x, self.y + deltay] != '.':
                posx = self.x + 1 if self.x + 1 < width - 1 else self.x - 1
            posy = self.y + deply 

        if math.fabs(dy) < ebomb_reach:
            posy = self.y
            if grid[self.x+deltax, self.y] != '.':
                posy = self.y + 1 if self.y + 1 < height - 1 else self.y - 1
            posx = self.x + deplx
            isNotMoved = False
        print("MOVE", posx, posy, sep=" ")



    # Method to update HERO actions
    def update(self, crates, walls):
        isUPDATE = False
        # Getting sense of direction
        change_x = self.x - self.past_x
        change_y = self.y - self.past_y

        print("changes:", change_x, change_y, self.past_x, self.past_y, self.x, self.y, sep=" ", file=sys.stderr)

        # Is HERO near a Wall or crate
        hero_wall_keys = []
        for k, wall in walls.items():
            if math.fabs(self.x - wall.x) == 1 or math.fabs(self.y - wall.y) == 1 :
                hero_wall_keys.append(k)
        hero_crate_keys = []
        for k, crate in crates.items():
            if math.fabs(self.x - crate.x) == 1 or math.fabs(self.y - crate.y) == 1 :
                hero_crate_keys.append(k)


        walls_list = [walls[x] for x in hero_wall_keys]
        crates_list = [crates[x] for x in hero_crate_keys]

        # Did we collide with a wall on our way to somewhere?
        for wall in walls_list:
            if math.fabs(wall.x - self.x) == 1 and change_x != 0:
                if change_y > 0:
                    newy = self.y+1 if self.y+1 < height-1 else self.y-1
                else:
                    newy = self.y-1 if self.y-1 > 0 else self.y+1
                isUPDATE = True
                print("MOVE", self.x, newy, sep=" ")
                break

            if math.fabs(wall.y - self.y) == 1 and change_y != 0:
                if change_x > 0:
                    newx = self.x+1 if self.x+1 < width-1 else self.x-1
                else:
                    newx = self.x-1 if self.x-1 > 0 else self.x+1
                isUPDATE = True
                print("MOVE", newx, self.y, sep=" ")
                break

        # Did we collide with a crate on our way to somewhere?
        for crate in crates_list:
            if math.fabs(crate.x - crate.x) == 1 and change_x != 0:
                if change_y > 0:
                    newy = self.y+1 if self.y+1 < height-1 else self.y-1
                else:
                    newy = self.y-1 if self.y-1 > 0 else self.y+1
                isUPDATE = True
                print("MOVE", self.x, newy, sep=" ")
                break

            if math.fabs(crate.y - crate.x) == 1 and change_y != 0:
                if change_x > 0:
                    newx = self.x+1 if self.x+1 < width-1 else self.x-1
                else:
                    newx = self.x-1 if self.x-1 > 0 else self.x+1
                isUPDATE = True
                print("MOVE", newx, self.y, sep=" ")
                break

        return isUPDATE
            

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
            grid[i,j] = row[j]
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
    hero_bombs = {}
    enemy_bombs = {}
    obj_ups = {}
    nb_hero_bombs = 0
    nebombs = 0
    nups = 0
    # Entities
    entities = int(input())
    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        # Populating each entity dictionaries
        if entity_type == 0 and owner == my_id:
            if isFirstTurn:
                hero.x = x
                hero.y = y
                isFirstTurn = False
            else:
                hero.past_x = hero.x
                hero.past_y = hero.y
                hero.x = x
                hero.y = y
            hero.param_1 = param_1
            hero.param_2 = param_2
        if entity_type == 2:
            obj_ups[nups] = Entity(entity_type, owner, x, y, param_1, param_2)
            nups += 1
        if entity_type == 1:
            if owner == my_id:
                hero_bombs[nb_hero_bombs] = Entity(entity_type, owner, x, y, param_1, param_2)
                nb_hero_bombs += 1
                hero.bomb_reach = param_2-1
                if (hero.x == x and hero.y == y):
                    isHeroOnABomb = True
            else:
                enemy_bombs[nebombs] = Entity(entity_type, owner, x, y, param_1, param_2)
                nebombs += 1
            
    # Populating the crates with near bomb dictionary
    crates_bombs = {}
    nb_crate_bomb = 0
    for k, crate in crates_dict.items():
        for k, bomb in hero_bombs.items():
            if math.fabs(bomb.x-crate.x) == 1 or math.fabs(bomb.y-crate.y) == 1:
                crates_bombs[nb_crate_bomb] = [crate.x, crate.y]

    '''
    ##### HERO Actions #####
        1- Is HERO threaten by enemy bombs?
        2- Is there close UPs to get?
        3- Move to close crate and bomb [repeat as many time as bomb available]
    '''
    # Is HERO next to a crate and have a bomb?
    if hero.param_1 != 0 and not hero.bomb_previous_turn and not isHeroOnABomb:
        isHeroNextCrate, posx_crate, posy_crate = hero.next_to_a_crate(crates_dict, crates_bombs)
        if isHeroNextCrate:
            hero.bomb_crate(posx_crate, posy_crate)
            print("HERO NEXT BOMB", file=sys.stderr)
            continue
    
    hero.bomb_previous_turn = False

    # Is HERO threaten by enemy bombs?
    if len(enemy_bombs) != 0:
        isHeroInDanger, posx_bomb, posy_bomb, ebomb_range = find_bombs_onboard(hero, enemy_bombs)
    if isHeroInDanger:
        hero.move_away_from_bombs(posx_bomb, posy_bomb, grid, ebomb_range)
        print("HERO DANGER", file=sys.stderr)
        continue

    # Is there close Ups to get?
    if len(obj_ups) != 0:
        isUpClose, posx_up, posy_up = find_ups_onboard(hero, obj_ups)
    if isUpClose:
        hero.move_to_ups(posx_up, posy_up)
        isUpClose = False
        print("HERO UP", file=sys.stderr)
        continue

    # No danger from close bombs and no close UPs to get, let's bomb some
    # crates!
    if len(crates_dict) == 0:
        print("No more crates", file=sys.stderr)
        print("MOVE 0 0")
    elif len(crates_dict) == 1:
        print("One crate left", file=sys.stderr)
        print("MOVE", int(width/2), int(height/2), sep=" ", file=sys.stderr)
    else:
        posx_crate, posy_crate = find_random_crate(crates_dict, crates_bombs)
        print("closest crate:", posx_crate, posy_crate, sep=" ", file=sys.stderr)
        if hero.param_1 != 0:
            deltax = posx_crate - hero.x
            deltay = posy_crate - hero.y
            print("deltas:", deltax, deltay, hero.bomb_reach, sep=" ", file=sys.stderr)
            if ((math.fabs(deltax) < hero.bomb_reach and deltay == 0) or (math.fabs(deltay) < hero.bomb_reach and deltax == 0)):
                # is there a wall between HERO and crate?
                isWallOnTheWay = False
                if deltax == 0:
                    start = hero.y if deltay < 0 else posy_crate
                    end = posy_crate if deltay < 0 else hero.y
                    if any(g == 'X' for g in grid[hero.x,start:end]):
                        isWallOnTheWay = True
                        print("Wall is on the way!! on y-axis", file=sys.stderr)
                    else:
                        isWallOnTheWay = False

                if deltay == 0:
                    start = hero.x if deltax < 0 else posx_crate
                    end = posx_crate if deltax < 0 else hero.x
                    if any(g != '.' or g !='X' for g in grid[start:end,hero.y]):
                        isWallOnTheWay = True
                        print("Wall is on the way!! on x-axis", file=sys.stderr)
                    else:
                        isWallOnTheWay = False

                if isWallOnTheWay:
                    posx_crate, posy_crate = find_random_crate(crates_dict, crates_bombs)
                    hero.move_to_crate(posx_crate, posy_crate)
                    print("HERO WALL BOMB", file=sys.stderr)
                else:
                    isBombUnderHero = False
                    isBombUnderHero = hero.bomb_under(enemy_bombs, hero_bombs)
                    if isBombUnderHero:
                        posx_crate, posy_crate = find_random_crate(crates_dict, crates_bombs)
                        print(posx_crate, posy_crate, sep=" ", file=sys.stderr)
                        hero.move_to_crate(posx_crate, posy_crate)
                        print("HERO MOVE", file=sys.stderr)
                    else:
                        hero.bomb_crate(posx_crate, posy_crate)
                        print("HERO BOMB", file=sys.stderr)
            else:
                hero.move_to_crate(posx_crate, posy_crate)
                print("HERO MOVE BOMB", file=sys.stderr)

        else:
            posx_crate, posy_crate = find_random_crate(crates_dict, crates_bombs)
            print(posx_crate, posy_crate, sep=" ", file=sys.stderr)
            hero.move_to_crate(posx_crate, posy_crate)
            print("HERO MOVE", file=sys.stderr)
