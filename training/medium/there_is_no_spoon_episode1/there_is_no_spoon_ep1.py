#!/opt/local/bin/python
"""
SOLUTION TO THE 'THERE IS NO SPOON EP1' PUZZLE

Version:
Created:
Compiler: python

Author: Dr. Samia Drappeau (SD), samia.drappeau@irap.omp.eu
Affiliation: IRAP/UPS, Toulouse, France
Notes: 
"""
import sys
import math

def search_neighbor_right(grid_line, i, j):
    idx_i = str(i)
    idx_j = None
    isNeighborFound = False
    dim = len(grid_line)
    for d in range(j+1,dim):
        if grid_line[d] == '0':
            isNeighborFound = True
            idx_j = str(d)
            break
        else:
            continue
    if (not isNeighborFound):
        idx_i = '-1'
        idx_j = '-1'
    
    return idx_i, idx_j


def search_neighbor_bottom(grid_column, i, j):
    idx_i = None
    idx_j = str(j)
    isNeighborFound = False
    dim = len(grid_column)
    for d in range(i+1,dim):
        if grid_column[d] == '0':
            isNeighborFound = True
            idx_i = str(d)
            break
        else:
            continue
    if (not isNeighborFound):
        idx_i = '-1'
        idx_j = '-1'

    return idx_i, idx_j


def main(argv):
    # Don't let the machines win. You are humanity's last hope...

    width = int(input())  # the number of cells on the X axis
    height = int(input())  # the number of cells on the Y axis

    # Saving the grid in a matrix
    grid = [['0' for j in range(width)] for i in range(height)]

    for i in range(height):
        line = list(input())
        for j in range(width):
            grid[i][j] = line[j]

    for i in range(height):
        for j in range(width):
            output = ''
            if grid[i][j] == '0':
                output += str(j) + ' ' + str(i) + ' '

                if (j != width-1):
                    # find neighbor right
                    idx_i, idx_j = search_neighbor_right(grid[i], i,j)
                    output += idx_j + ' ' + idx_i + ' '
                else:
                    output += '-1 -1 '
                if (i != height-1):
                    # find neighbor bottom
                    column = [row[j] for row in grid]
                    idx_i, idx_j= search_neighbor_bottom(column, i,j)
                    output += idx_j + ' ' + idx_i
                else:
                    output += '-1 -1'
                print(output)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

