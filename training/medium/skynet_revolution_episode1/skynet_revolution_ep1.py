#!/opt/local/bin/python
"""
SOLUTION TO THE 'SKYNET REVOLUTION EPISODE 1' PUZZLE

Version:    1.0
Created:    10/02/2016
Compiler:   python3.5

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Notes: 
"""
import sys
import math


def bfs(graph, start, end):
    """
    A Breadth-first search
    
    keywords:
    graph   the graph to search
    start   start node of the search
    end     end node of the search


    example of use:
        graph = {
        '1': ['2', '3', '4'],
        '2': ['5', '6'],
        '5': ['9', '10'],
        '4': ['7', '8'],
        '7': ['11', '12']
        }
        print bfs(graph, '1', '11')
    """
    # Queue of paths
    queue = []
    
    # pushing the first path into the queue
    queue.append([start])
    
    while queue:
        # getting the first path from the queue
        path = queue.pop(0)
        
        # getting the last node of the path
        node = path[-1]
        
        if node == end:
            # we have found the path
            return path
        
        # find all neighbouring nodes, construct new paths for each and save them to queue 
        for neighbour in graph.get(node, []):
            new_path = list(path)
            new_path.append(neighbour)
            queue.append(new_path)
    

class Node(object):
    """A class representing a node.
    Each node is characterized by a unique id.
    It also has the list of its neighbours.
    """
    def __init__(self, node_id=0):
        self.node_id = node_id
        self.neighbours = []
        
    def addNeighbour(self, node_id):
        self.neighbours.append(node_id)
    
    def removeNeighbour(self, node_id):
        self.neighbours.remove(node_id)
        
        
class Path(object):
    


# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in input().split()]
print(n,l,e, sep=" ", file=sys.stderr)
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    print(n1, n2, sep=" ", file=sys.stderr)
for i in range(e):
    ei = int(input())  # the index of a gateway node
    print(ei, sep=" ", file=sys.stderr)

graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}

# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
    print("virus", si, sep=" ", file=sys.stderr)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # Example: 0 1 are the indices of the nodes you wish to sever the link between
    print("1 2")


