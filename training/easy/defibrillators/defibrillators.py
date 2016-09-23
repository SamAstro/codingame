#!/opt/local/bin/python
"""
SOLUTION TO THE 'DEFIBRILLATORS' PUZZLE

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

def deg2rad(angle):
    return (angle*math.pi/180)


def main(argv):
    lon = deg2rad(float(input().replace(',','.')))
lat = deg2rad(float(input().replace(',','.')))
n = int(input())

# Let's save the defib into a dictionary
defib_catalog = {}
defib_category = ["Name", "Address", "Phone", "Longitude", "Latitude"]
for i in range(n):
    defib = input()
    defib_id, defib_name, defib_address, defib_phone, defib_long, defib_lat = defib.split(";")
    # Replace comma to dot in number and convert to radian
    defib_long = deg2rad(float(defib_long.replace(',','.')))
    defib_lat = deg2rad(float(defib_lat.replace(',','.')))
    defib_info = [defib_name, defib_address, defib_phone, defib_long, defib_lat]
    # Save in dictionary
    defib_catalog[defib_id] = {}
    for i, cat in enumerate(defib_category):
        defib_catalog[defib_id][cat] = defib_info[i]
        
dist = 1e10
dfid = None
for dfib_id, dfib_info in defib_catalog.items():
    x = (lon - dfib_info["Longitude"]) * math.cos((dfib_info["Latitude"] + lat)/2)
    y = lat - dfib_info["Latitude"]
    distance = math.sqrt(x**2 + y**2) * 6371
    
    if distance != dist:
        if distance < dist:
            dist = distance
            dfid = dfib_id
        else:
            pass
    
print(defib_catalog[dfid]["Name"])


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

