#!/opt/local/bin/python
"""
DESCRIPTION OF THE SCRIPT

Version:
Created:
Compiler: python

Author: Dr. Samia Drappeau (SD), samia.drappeau@irap.omp.eu
Affiliation: IRAP/UPS, Toulouse, France
Notes: 
"""
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def locate_min(a):
    smallest = min(a)
    return smallest, [index for index, element in enumerate(a) if smallest == element]


def main(argv):

    try:
        n = int(input())  # the number of temperatures to analyse
        temps = input().split()  # the n temperatures expressed as integers ranging from -273 to 5526
       
       
        # Convert string to integer
        temps = list(map(int, temps))
        temps_abs = list(map(abs, temps))
        
        # Find the minimal abs value in list
        # Make sure if we have -min and min, we choose min.
        ## We need this if-else condition to find the negative minimum when
        ## existing

        min, indices = locate_min(temps_abs)
        if len(indices) == 1:
            res = min(temps, key=lambda x:abs(x))
        else:
            if all(temps[idx] < 0 for idx in indices):
                res = locate_min(temps)[0]
            else:
                res = locate_min(temps_abs)[0]
        
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

        print(res)

    except ValueError:
        print("0")



if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

