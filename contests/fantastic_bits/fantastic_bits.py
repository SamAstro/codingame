"""
DESCRIPTION OF THE SCRIPT

Version:
Created:
Compiler: python

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Affiliation:
Notes: 
"""

import sys
import math
import numpy as np
import random

from heapq import *

# Reproducing randomness -- FOR DEBUG ONLY
random.seed(9001)

# Manhattan distance: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#S7
#function heuristic(node) =
#    dx = abs(node.x - goal.x)
#    dy = abs(node.y - goal.y)
#    return D * (dx + dy)

def distance(wiz, snaf):
    dx = snaf.x - wiz.x
    dy = snaf.y - wiz.y
    dist = math.fabs(dx) + math.fabs(dy)
    return dist

def distance_goal(goal, snaf):
    dx = snaf.x - goal[0]
    dy = snaf.y - goal[1]
    dist = math.fabs(dx) + math.fabs(dy)
    return dist


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

    def set_magic(self, spell_cost = 0, turn_magic_pt = 1, init=False):
        '''
        Track magic level
        '''
        if init:
            self.magic_lvl = 1
        else:
            self.magic_lvl += turn_magic_pt - spell_cost



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
    to_snaf = 1e5
    snafid = None
    prev_action = None

    def __init__(self, entity_id, entity_type, x, y, vx, vy, state):
        super().__init__(entity_id, entity_type, x, y, vx, vy, state)

    def set_prev_action(self, action):
        wiz.prev_action = action

    def cast_spell(self,spell, entity_id):
        print(spell, str(entity_id), sep=" ")


class Bludger(Entity):
    def __init__(self, entity_id, entity_type, x, y, vx, vy, state):
        super().__init__(entity_id, entity_type, x, y, vx, vy, state)






# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left

game = Game_Status(my_team_id)

game.set_goal()

game.set_magic(init=True)


# game loop
while True:
    game.reset()

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

    wiz_has_not_cast = True
    used_snaffle = []
    spell_cost = 0
    for wizid, wiz in game.wizard.items():
        if game.magic_lvl > 20 and wiz_has_not_cast:#and (wiz.prev_action == 'THROW' and wiz.snafid in game.snaffle.values()):
            wiz.DEST = [-99, -99]

            # Find closest snaf to wiz and to goal
            snaf_to_goal_id = None
            snaf_to_goal_dist = 1e5

            for snafid, snaf in game.snaffle.items():
                dist = distance(wiz, snaf)
                if dist < wiz.to_snaf:
                    wiz.to_snaf = dist
                    wiz.snaffle_id = snafid

                dist_goal = distance_goal(game.own_goal_pos, snaf)
                if dist_goal < snaf_to_goal_dist:
                    snaf_to_goal_dist = dist_goal
                    snaf_to_goal_id = snafid

            # Protect first own goal
            if snaf_to_goal_dist <= 4000:
                wiz.action = 'PETRIFICUS'
                wiz.snafid = game.snaffle[snaf_to_goal_id].entity_id
                spell_cost = 10
            else:
                diffx = wiz.x - game.snaffle[wiz.snaffle_id].x if game.goal_dir == 'LEFT' else game.snaffle[wiz.snaffle_id].x - wiz.x
                print(wiz.x, game.snaffle[wiz.snaffle_id].x, diffx, sep=" ", file=sys.stderr)
                if diffx >= 0:
                    wiz.action = 'FLIPENDO'
                    spell_cost = 20
                else:
                    wiz.action = 'PETRIFICUS'
                    spell_cost = 10
                wiz.snafid = game.snaffle[wiz.snaffle_id].entity_id
            wiz_has_not_cast = False
            used_snaffle.append(wiz.snafid)
        else:

            if wiz.state == 0:
                wiz.action = "MOVE"
                # Find closest snaffle to wizard
                for snafid, snaf in game.snaffle.items():
                    if game.snaffle[snafid].entity_id in used_snaffle:
                        continue
                    else:
                        dist = distance(wiz, snaf)
                        if dist < wiz.to_snaf:
                            wiz.to_snaf = dist
                            wiz.snaffle_id = snafid
                
                used_snaffle.append(game.snaffle[wiz.snaffle_id].entity_id)
                wiz.DEST = [game.snaffle[wiz.snaffle_id].x, game.snaffle[wiz.snaffle_id].y]
                wiz.power = '150'
            else:
                wiz.action = "THROW"
                wiz.DEST = game.goal_pos
                wiz.power = '500'

        if wiz.DEST[0] == -99 or wiz.DEST[1] == -99:
            print(wiz.action, wiz.snafid, sep=" ")
            game.set_magic(spell_cost = spell_cost)
        else:
            print(wiz.action, wiz.DEST[0], wiz.DEST[1], wiz.power, sep=" ")

    print(game.magic_lvl, file=sys.stderr)
    game.set_magic()
