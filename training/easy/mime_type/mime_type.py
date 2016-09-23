#!/opt/local/bin/python
"""
SOLUTION TO THE "MIME TYPE" PUZZLE

Version:    1.0
Created:    09/23/2016
Compiler:   python 3.5

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Notes: 
"""
import sys
import math
 
def get_extension(fname):
    file_element = fname.lower().split(".")
    if len(file_element) != 1:
        file_extension = file_element[-1]
    else:
        file_extension = 'None'
    return file_extension

def main(argv):
    n = int(input())  # Number of elements which make up the association table.
    q = int(input())  # Number Q of file names to be analyzed.

    # Let's save the association table into a dictionary
    asso_dict = {}
    for i in range(n):
        # ext: file extension
        # mt: MIME type.
        ext, mt = input().split()
        asso_dict[ext.lower()] = mt

    for i in range(q):
        fname = input()  # One file name per line.
        file_ext = get_extension(fname)
        if file_ext in asso_dict:
            print(asso_dict[file_ext])
        else:
            print("UNKNOWN")


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

