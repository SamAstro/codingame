#!/opt/local/bin/python
"""
SOLUTION OF THE 'HORSE-RACING DUALS' PUZZLE

Version:    1.0
Created:    09/23/2016
Compiler:   python3.5

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Notes: 
"""
import sys
import math
import bisect

def main(argv):
    # Auto-generated code below aims at helping you parse
    # the standard input according to the problem statement.

    minimum = 1e5
    diff = 0
    n = int(input())

    # We are going to fill in the list of strenghts sorted.
    strenght_horses = []
    for i in range(n):
        pi = int(input())
        bisect.insort(strenght_horses,pi)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    for i in range(n-1):
        diff = strenght_horses[i+1] - strenght_horses[i]
        if diff < minimum:
            minimum = diff

    print(minimum)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

