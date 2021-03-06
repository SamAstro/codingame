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
isFirstBomb = True

# Reproducing randomness -- FOR DEBUG ONLY
random.seed(9001)

##### FUNCTIONS #####
def distance(hero, cx, cy):
    distx = math.sqrt((cx - hero.x)**2)
    disty = math.sqrt((cy - hero.y)**2)
    return distx, disty

def find_crate(crates, crates_bombs, random=True):
    posx, posy = 0, 0
    isCrateFound = False
    mdist = 30

    if len(crates) == 0:
        isCrateFound = True
        posx = random.randint(0,13)
        posy = random.randint(0,11)
    elif len(crates) == 1:
        isCrateFound = True
        posx = crates[0].x
        posy = crates[0].y
    else:
        while not isCrateFound:
            if random:
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
            else:
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
                        dist = dx + dy
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

def find_bot_onboard(hero, bots):
    posx, posy = 0,0
    isBotNear = False
    for k, bot in bots.items():
        dx = hero.x - bot.x
        dy = hero.y - bot.y
        if (math.fabs(dx) < hero.bomb_reach and dy == 0) or (math.fabs(dy) < hero.bomb_reach and dx == 0):
            isBotNear = True
            posx = bot.x
            posy = bot.y
    return isBotNear, posx, posy


def find_bombs_onboard(hero, bombs):
    bomb_range = None
    posx, posy = 0,0
    isHeroInDanger = False
    for k,bomb in bombs.items():
        bomb_range = bomb.param_2 - 1
        bomb_timer = bomb.param_1
        bomb_constraint = 2 #max(bomb_range, ebomb_timer)
        dx = hero.x - bomb.x
        dy = hero.y - bomb.y
        if (dy == 0 or dx == 0) or (dy == 1 or dx == 1):
        #if (math.fabs(dx) < ebomb_constraint and dy == 0) or (math.fabs(dy) < ebomb_constraint and dx == 0):
            isHeroInDanger = True
            posx = bomb.x
            posy = bomb.y
    return isHeroInDanger, posx, posy, bomb_range



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
    def move_away_from_bombs(self, posx_bomb, posy_bomb, grid, ebomb_reach=2):
        posx = 0
        posy = 0

        deplx = 1 if self.x + 1 < width - 1 else -1
        deply = 1 if self.y + 1 < height - 1 else -1


        dx = self.x - posx_bomb
        dy = self.y - posy_bomb

        if dx == 0:
            # Hero and bot bomb on same column.
            # Need to move Hero to next column
            posx = self.x + 1 if self.x + 1 < width - 1 else self.x - 1
            if dy > 0:
                posy = self.y + 1 if self.y + 1 < height-1 else self.y - 1
            else:
                posy = self.y - 1 if self.y - 1 > 0 else self.y + 1

            # Is not square available?
            if grid[posy, posx] != '.':
                posy = self.y + 2 if self.y + 2 < height - 1 else self.y - 2

        elif dy == 0:
            if dx > 0:
                posx = self.x + 1 if self.x + 1 < width - 1 else self.x - 1
            else:
                posx = self.x - 1 if self.x - 1 > 0 else self.x + 1

            posy = self.y + 1 if self.y + 1 < height-1 else self.y - 1
            if grid[posy, posx] != '.':
                posx = self.x + 2 if self.x + 2 < width - 1 else self.x - 2
        else:
            print("already in safe place, do not move", file=sys.stderr)
            posx = self.x
            posy = self.y

        print("MOVE", posx, posy, sep=" ")



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
    print('Turn begins...', file=sys.stderr)
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

    print('Crates and wall populated...', file=sys.stderr)

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
    print("entities loaded", entities, sep=" ", file=sys.stderr)

    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        # Populating each entity dictionaries
        print("entities split", entity_type, owner, x, y, param_1, param_2, sep=" ", file=sys.stderr)

        if entity_type == 0:
            if owner == my_id:
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
            else:
                bots[nbots] = Entity(entity_type, owner, x, y, param_1, param_2)
                nbots += 1

        print("entities bot or hero", file=sys.stderr)

        if entity_type == 2:
            obj_ups[nups] = Entity(entity_type, owner, x, y, param_1, param_2)
            nups += 1

        print("entities up", file=sys.stderr)

        if entity_type == 1:
            all_bombs[nb_bombs] = Entity(entity_type, owner, x, y, param_1, param_2)
            nb_bombs += 1
            print("bomb added", file=sys.stderr)
            if hero.x == x and hero.y == y:
                isHeroOnABomb = True
                print("hero on bomb", file=sys.stderr)
            if owner == my_id:
                hero.bomb_reach = param_2-1
                print("reach bomb", file=sys.stderr)
            
    print('Entities done...', file=sys.stderr)

    # Populating the crates with near bomb dictionary
    crates_bombs = {}
    nb_crate_bomb = 0
    for k, crate in crates_dict.items():
        for k, bomb in all_bombs.items():
            if math.fabs(bomb.x-crate.x) == 1 or math.fabs(bomb.y-crate.y) == 1:
                crates_bombs[nb_crate_bomb] = [crate.x, crate.y]

    print('crates and crates bomb done...', file=sys.stderr)

    '''
    ##### HERO Actions #####
        -- is HERO threaten by bombs?
            yes -- go to safe place
            no -- HERO attacks: does HERO has bomb left?
                yes -- is there VILLAIN closeby?
                    yes -- BOMB VILLAIN
                    no -- is there CRATE nearby?
                        yes -- is there wall between HERO and CRATE?
                            yes -- [repeat - is there CRATE nearby]
                            no -- BOMB CRATE
                        no -- is there UPs nearby?
                            yes -- MOVE UP
                            no -- MOVE RANDOM CRATE
                no -- go to safe place or RANDOM CRATE
    '''
    print("Starting Turn Action...", file=sys.stderr)
    if isFirstBomb:
        print("Putting first Bomb", file=sys.stderr)
        posx_crate, posy_crate = find_crate(crates_dict, crates_bombs, random=False)
        hero.bomb_crate(posx_crate, posy_crate)
        isFirstBomb = False
    else:
        if len(all_bombs) != 0:
            print("Bombs are on board", file=sys.stderr)
            isHeroInDanger, posx_bomb, posy_bomb, ebomb_range = find_bombs_onboard(hero, bombs)
        if isHeroInDanger:
            # HERO plays defence
            hero.move_away_from_bombs(posx_bomb, posy_bomb, grid, ebomb_range)
            print("HERO DANGER", file=sys.stderr)
        else:
            if hero.param_1 != 0:
                # HERO plays attack
                isBotNear, posx_bot, posy_bot = find_bot_onboard(hero,bots)
                if isBotNear:
                    print("BOMB", posx_bot, posy_bot, sep=" ")
                else:
                    if len(crates_dict) == 0:
                        print("No more crates", file=sys.stderr)
                        print("MOVE", hero.x, hero.y, sep=" ", file=sys.stderr)
                    else:
                        # HERO close to crate?
                        print(hero.bomb_previous_turn, isHeroOnABomb, sep=" ", file=sys.stderr)
                        isHeroNextCrate = False
                        if not hero.bomb_previous_turn and not isHeroOnABomb:
                            isHeroNextCrate, posx_crate, posy_crate = hero.next_to_a_crate(crates_dict, crates_bombs)
                        if isHeroNextCrate:
                            hero.bomb_crate(posx_crate, posy_crate)
                            hero.bomb_previous_turn = False
                        else:
                            if len(obj_ups) != 0:
                                isUpClose, posx_up, posy_up = find_ups_onboard(hero, obj_ups)
                            if isUpClose:
                                hero.move_to_ups(posx_up, posy_up)
                                isUpClose = False
                            else:
                                posx_crate, posy_crate = find_crate(crates_dict, crates_bombs, random=False)
                                hero.move_to_crate(posx_crate, posy_crate)
            else:
                posx_crate, posy_crate = find_crate(crates_dict, crates_bombs)
                hero.move_to_crate(posx_crate, posy_crate)


