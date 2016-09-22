#!/opt/local/bin/python
"""
SOLUTION OF THE 'ASCII ART' PUZZLE

Version:    1.0
Created:    09/22/2016
Compiler:   python3.5

Author: Dr. Samia Drappeau (SD), drappeau.samai@gmail.com
Notes: 
"""
import sys
import math

# Print letter in ascii art
def letter_ascii(row, letter_idx, height, lenght):
    return [row[j:j + l] for j in range(0, len(row), lenght)][letter_idx]


def find_letter_idx(char):
    if (ord(char) >= ord('a')) and (ord(char) <= ord('z')):
        idx = ord(char) - 97
    else:
        idx = ord('z') + 1 - 97
    return idx


def main(argv):
    # Auto-generated code below aims at helping you parse
    # the standard input according to the problem statement.

    l = int(input())
    h = int(input())
    t = input().lower()

    alphabet = []
    # Save the alphabet
    for i in range(h):
        row = input()
        alphabet.append(row)
        
    # Express letter index for each letter in the word
    char_idx = []

    for char in t:
        char_idx.append(find_letter_idx(char))
        
        
    # Printing the word:
    for i in range(h):
        row = alphabet[i]
        for idx in range(len(t)):
            print(letter_ascii(row, char_idx[idx], h, l),end="")
        print()


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

