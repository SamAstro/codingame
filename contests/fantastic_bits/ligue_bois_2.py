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

#####################
###### Classes ######
#####################
class Entity():
    DEST = [0,0]
    action = None
    power = 150
    snaffle_id = 0
    to_snaf = 1e5

    def __init__(self, entity_id, entity_type, x, y, vx, vy, state):
        self.id = entity_id
        self.type = entity_type
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.state = state


# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left

goal_pos = [0,0]
# Decide where to throw Snaffle
if my_team_id == 1:
    goal_pos = [0,3750]
else:
    goal_pos = [16000,3750]


# game loop
while True:
    # Dictionaries saving each entity types
    wizard = {}
    opp_wizard = {}
    snaffle = {}
    bludger = {}
    nwiz = 0
    noppwiz = 0
    nsnaffle = 0
    nbludger = 0

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
            wizard[nwiz] = Entity(entity_id, entity_type, x, y, vx, vy, state)
            nwiz += 1
        elif entity_type == 'OPPONENT_WIZARD':
            opp_wizard[noppwiz] = Entity(entity_id, entity_type, x, y, vx, vy, state)
            noppwiz += 1
        elif entity_type == 'SNAFFLE':
            snaffle[nsnaffle] = Entity(entity_id, entity_type, x, y, vx, vy, state)
            nsnaffle += 1
        elif entity_type == 'BLUDGER':
            bludger[nbludger] = Entity(entity_id, entity_type, x, y, vx, vy, state)
            nbludger += 1
        else:
            print("Wrong type of entity", file=sys.stderr)

    


    for wizid, wiz in wizard.items():
        if wiz.state == 0:
            wiz.action = "MOVE"

            # Find closest snaffle to wizard
            for snafid, snaf in snaffle.items():
                dist = distance(wiz, snaf)
                if dist < wiz.to_snaf:
                    wiz.to_snaf = dist
                    wiz.snaffle_id = snafid
            
            wiz.DEST = [snaffle[wiz.snaffle_id].x, snaffle[wiz.snaffle_id].y]
            wiz.power = '150'
        else:
            wiz.action = "THROW"
            wiz.DEST = goal_pos
            wiz.power = '500'

        print(wiz.action, wiz.DEST[0], wiz.DEST[1], wiz.power, sep=" ")
