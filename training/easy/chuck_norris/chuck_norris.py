#!/opt/local/bin/python
"""
SOLUTION TO THE 'CHUCK NORRIS' PUZZLE

Version:    1.0
Created:    09/23/2016
Compiler:   python 3.5

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Notes: 
"""
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def ascii_to_binary(msg_ascii):
    msg_binary = msg_ascii.encode('ascii')
    return (format(msg_b, '07b') for msg_b in msg_binary)

def binary_to_unary(msg_binary):
    previous_nb = None
    count = 0
    for nb in msg_binary:
        if nb != previous_nb:
            print(('0'*count) +\
            (' ' if count else '') +\
            ("00 " if nb == '0' else "0 "), end='')
            count  = 1
        else:
            count += 1
        previous_nb = nb
    print("0"*count, end="")

    
def ascii_to_unary(msg_ascii):
    msg_b = ""
    for msg in ascii_to_binary(msg_ascii):
        msg_b += msg
    binary_to_unary(msg_b)

def main(argv):
    message = input()
    print(message, file=sys.stderr)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    ascii_to_unary(message)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

