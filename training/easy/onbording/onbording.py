#!/opt/local/bin/python
"""
SOLUTION TO THE 'ONBOARDING' PUZZLE -- CODINGAME.COM

Version: 1
Created: 09/21/2016
Compiler: python 3.5

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Notes: 
"""

def main(argv):

# game loop
while 1:
    enemy_1 = input()  # name of enemy 1
    dist_1 = int(input())  # distance to enemy 1
    enemy_2 = input()  # name of enemy 2
    dist_2 = int(input())  # distance to enemy 2

    if dist_1 < dist_2:
        print(enemy_1)
    else:
        print(enemy_2)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

