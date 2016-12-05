#!/opt/local/bin/python
"""
SOLUTION TO THE 'MARS LANDER - EP2' PUZZLE

Version:    1.0
Created:    12/01/2016
Compiler:   python 3.5

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Notes: 
"""
import sys
import math    

GRAVITY = 3.711 #m/s

class Surface():
    def __init__(self, point, aligned_with_previous

class Point():
    ''' Point class represents and manipulates x,y coordinates'''
    def __init__(self, x = 0, y = 0):
        ''' Create a new point at x, y'''
        self.x = x
        self.y = y

    def sqDistance(self, point = Point()):
        return ((self.x - point.x)*(self.x - point.x) + (self.y - point.y)*(self.y - point.y))

    def distance(self, point = Point()):
        return math.sqrt(sqDistance(self, point))


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

surface_n = int(input())  # the number of points used to draw the surface of Mars.
surface = {}

for i in range(surface_n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]
    surface[i] = Point(land_x, land_y)


# First thing first, we need to find the landing spot!



# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]

    power_str = "0"
    if abs(v_speed) > 38:
        power_str = "4"
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # 2 integers: rotate power. rotate is the desired rotation angle (should be 0 for level 1), power is the desired thrust power (0 to 4).
    print("0 " + power_str)
