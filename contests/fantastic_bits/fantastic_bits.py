"""
BOT FOR THE 'FANTASTIC BITS' [CG] CONTEST

Version:
Created:
Compiler: python

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Affiliation:
Notes: 
"""

import sys
import math
import random

ARENA_MAX_X = 16001
ARENA_MAX_Y = 7501

def distance(wiz, entity):
    dx = (entity.x - wiz.x)*(entity.x - wiz.x)
    dy = (entity.y - wiz.y)*(entity.y - wiz.y)
    dist = dx + dy
    return dist

def findFarthest(wiz, entities, used_entities=[]):
    ''' Find closest entity to my wizard.'''
    max_distance = sys.float_info.max
    farthest_entity = None
    for entity_id, entity in entities.items():
        if entities[entity_id].entity_id in used_entities:
            continue
        else:
            dist = distance(wiz, entity)
            if farthest_entity == None or dist > max_distance:
                max_distance = dist
                farthest_entity = entities[entity_id]
    return farthest_entity

def findClosest(wiz, entities, used_entities=[]):
    ''' Find closest entity to my wizard.'''
    min_distance = 0
    closest_entity = None
    for entity_id, entity in entities.items():
        if entities[entity_id].entity_id in used_entities:
            continue
        else:
            dist = distance(wiz, entity)
            if closest_entity == None or dist < min_distance:
                min_distance = dist
                closest_entity = entities[entity_id]
    return closest_entity

def collinear(a, b, c):
    ''' Return True if a, b, and c are all on the same line.'''
    return (b.x - a.x) * (c.y - a.y) == (c.x - a.x) * (b.y - a.y)

def is_entities_blocking(wiz, closest_snaffle, entities, my_team_id):
    ''' Are the entities, the wizard and the closest_snaffle on the same line?'''
    entity_blocking = False
    for entity_id, entity in entities.items():
        if (entity.entity_type == closest_snaffle.entity_type and entity.entity_id == closest_snaffle.entity_id) or (entity.entity_type == wiz.entity_type and entity.entity_id == wiz.entity_id):
            continue
        else:
            are_wiz_snaf_entity_collinear = collinear(wiz, closest_snaffle, entity)
            dx = wiz.x - entity.x if my_team_id == 1 else entity.x - wiz.x
            if are_wiz_snaf_entity_collinear and dx > 0:
                entity_blocking = True
            else:
                continue
    return entity_blocking

def is_entities_ontheway(wiz, opp_goal, entities, my_team_id):
    ''' Are the entities, the wizard and the closest_snaffle on the same line?'''
    entity_blocking = False
    for entity_id, entity in entities.items():
        are_wiz_snaf_entity_collinear = collinear(wiz, opp_goal, entity)
        dx = wiz.x - entity.x if my_team_id == 1 else entity.x - wiz.x
        
        if are_wiz_snaf_entity_collinear and dx > 0:
            entity_blocking = True
        else:
            continue
    return entity_blocking
        

def is_entities_aligned(wiz, closest_snaffle, opp_goal):
    dx = closest_snaffle.x - wiz.x
    dy = closest_snaffle.y - wiz.y
    
    if dx < 1000:
        return False
    else:
        slope = dy/dx
        dest_y = closest_snaffle.y + (opp_goal.x - closest_snaffle.x) * slope

        if dest_y < 0:
            dest_y = -dest_y
        elif dest_y > ARENA_MAX_Y:
            dest_y = 2*ARENA_MAX_Y - dest_y 
        else:
            pass
        return math.fabs(dest_y - opp_goal.y) < opp_goal.width / 2 + opp_goal.pole_radius


def is_snaffle_infront(wiz, closest_snaffle, my_team_id):
    if my_team_id == 0:
        if closest_snaffle.x - wiz.x > 0:
            return True
        else:
            return False
    else:
        if closest_snaffle.x - wiz.x < 0:
            return True
        else:
            return False


def is_snaffle_behind(wiz, closest_snaffle, my_team_id):
    if my_team_id == 0:
        if closest_snaffle.x - wiz.x < 0:
            return True
        else:
            return False
    else:
        if closest_snaffle.x - wiz.x > 0:
            return True
        else:
            return False




"""
Classes

"""
class Game_Status():
    def __init__(self, my_team_id, wizard = {}, opp_wizard = {}, snaffle = {}, bludger ={},\
                 nwiz = 0, noppwiz = 0,\
                 nsnaffle = 0, nbludger = 0):
        self.wizard = wizard
        self.opp_wizard = opp_wizard
        self.snaffle = snaffle
        self.bludger = bludger
        self.nwiz = nwiz
        self.noppwiz = noppwiz
        self.nsnaffle = nsnaffle
        self.nbludger = nbludger
        self.my_team_id = my_team_id

    def reset(self):
        self.wizard.clear()
        self.opp_wizard.clear()
        self.snaffle.clear()
        self.bludger.clear()
        self.nwiz = 0
        self.noppwiz = 0
        self.nsnaffle = 0
        self.nbludger = 0


    def set_goal(self):
        '''
        Decide where to throw Snaffle
        '''
        if self.my_team_id == 1:
            self.goal_pos = [0,3750]
            self.own_goal_pos = [16000,3750]
            self.goal_dir = 'LEFT'
        else:
            self.goal_pos = [16000,3750]
            self.own_goal_pos = [0,3750]
            self.goal_dir = 'RIGHT'



    def set_magic(self, spell_cost = 0, turn_magic_pt = 0, init=False):
        '''
        Track magic level
        '''
        if init:
            self.mana_lvl = 0
        else:
            self.mana_lvl += turn_magic_pt - spell_cost



class Entity():
    def __init__(self, entity_id, entity_type, x, y, vx, vy, state):
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.state = state

class Snaffle(Entity):
    def __init__(self, entity_id, entity_type, x, y, vx, vy, state):
        super().__init__(entity_id, entity_type, x, y, vx, vy, state)


class Wizard(Entity):
    action = None
    DEST = [0,0]
    power = 150
    snaffle_id = 0
    to_snaf = 1e9
    snafid = None
    prev_action = None
    msg = None

    def __init__(self, entity_id, entity_type, x, y, vx, vy, state):
        super().__init__(entity_id, entity_type, x, y, vx, vy, state)

    def set_prev_action(self, action):
        wiz.prev_action = action

    def cast_spell(self, spell, entity_id):
        print(spell, str(entity_id), sep=" ")

    def play(self, spell_cost):
        if self.DEST[0] == -99 or wiz.DEST[1] == -99:
            self.cast_spell(self.action, self.snafid)
            game.set_magic(spell_cost = spell_cost)
        else:
            if self.msg == None:
                print(self.action, self.DEST[0], self.DEST[1], self.power, sep=" ")
            else:
                print(self.action, self.DEST[0], self.DEST[1], self.power, self.msg, sep=" ")

    def throw_action(self, opp_goal):
        self.power = '500'
        self.action = 'THROW'
        self.DEST = [opp_goal.x, opp_goal.y]

    def move_action(self, entity):
        self.power = '150'
        self.action = 'MOVE'
        self.DEST = [entity.x, entity.y]

    def find_best_snaffle_to_flipendo(self, snaffles, opp_wizards, wizards, bludgers, opp_goal, my_team_id):
        for snafid, snaf in snaffles.items():
            target_aligned = is_entities_aligned(wiz, snaf, opp_goal)
            bludger_blocking = is_entities_blocking(wiz, snaf, bludgers, my_team_id)
            snaffle_blocking = is_entities_blocking(wiz, snaf, snaffles, my_team_id)
            mywiz_blocking = is_entities_blocking(wiz, snaf, wizards, my_team_id)
            opp_wiz_blocking = is_entities_blocking(wiz, snaf, opp_wizards, my_team_id)
            if is_snaffle_infront(wiz, snaf, my_team_id) and target_aligned and (not bludger_blocking) and (not snaffle_blocking) and (not mywiz_blocking) and (not opp_wiz_blocking):
                return snaf
            else:
                return None


class Bludger(Entity):
    def __init__(self, entity_id, entity_type, x, y, vx, vy, state):
        super().__init__(entity_id, entity_type, x, y, vx, vy, state)


class Goal():
    width = 4000
    pole_radius = 400
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left

game = Game_Status(my_team_id)

my_goal = Goal(16000 if my_team_id == 1 else 0, 3750)

opp_goal = Goal(0 if my_team_id == 1 else 16000, 3750)


game.set_magic(init=True)

turn = 0

# game loop
while True:
    turn += 1
    game.reset()

    print(game.mana_lvl, turn, sep=' ', file=sys.stderr)

    # Entities
    entities = int(input())  # number of entities still in game

    # Populate entities
    for i in range(entities):
        # entity_id: entity identifier
        # entity_type: "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        # x: position
        # y: position
        # vx: velocity
        # vy: velocity
        # state: 1 if the wizard is holding a Snaffle, 0 otherwise
        entity_id, entity_type, x, y, vx, vy, state = input().split()
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        state = int(state)

        if entity_type == 'WIZARD':
            game.wizard[game.nwiz] = Wizard(entity_id, entity_type, x, y, vx, vy, state)
            game.nwiz += 1
        elif entity_type == 'OPPONENT_WIZARD':
            game.opp_wizard[game.noppwiz] = Wizard(entity_id, entity_type, x, y, vx, vy, state)
            game.noppwiz += 1
        elif entity_type == 'SNAFFLE':
            game.snaffle[game.nsnaffle] = Snaffle(entity_id, entity_type, x, y, vx, vy, state)
            game.nsnaffle += 1
        elif entity_type == 'BLUDGER':
            game.bludger[game.nbludger] = Bludger(entity_id, entity_type, x, y, vx, vy, state)
            game.nbludger += 1
        else:
            print("Wrong type of entity", file=sys.stderr)


    used_snaffle = []
    spell_cost = 0

    for wizid, wiz in game.wizard.items():
        best_snaffle = wiz.find_best_snaffle_to_flipendo(game.snaffle, game.opp_wizard, game.wizard, game.bludger, opp_goal, my_team_id)
        farthest_snaffle = findFarthest(wiz, game.snaffle, used_snaffle)
        dist_wiz_snaffle = distance(wiz, farthest_snaffle)

        if wiz.state == 1:
            wiz.throw_action(opp_goal)
        elif game.mana_lvl >= 20 and best_snaffle != None:
                wiz.DEST = [-99, -99]
                wiz.action = 'FLIPENDO'
                spell_cost = 20
                wiz.snafid = best_snaffle.entity_id
                used_snaffle.append(best_snaffle.entity_id)
        elif game.mana_lvl >= 20 and is_snaffle_behind(wiz, farthest_snaffle, my_team_id) and dist_wiz_snaffle > 2000*2000:
            wiz.DEST = [-99, -99]
            if game.nsnaffle == 1:
                wiz.action = 'PETRIFICUS'
                spell_cost = 10
            else:
                wiz.action = 'ACCIO'
                spell_cost = 20
            wiz.snafid = farthest_snaffle.entity_id
            used_snaffle.append(farthest_snaffle.entity_id)
        else:
            # find closest snaffle to move to.
            closest_snaffle = findClosest(wiz, game.snaffle, used_snaffle)
            wiz.move_action(closest_snaffle)
            used_snaffle.append(closest_snaffle.entity_id)


        if game.nsnaffle <= 2:
            used_snaffle = []

        wiz.play(spell_cost)
        
    game.set_magic(turn_magic_pt=1)
