"""
Should we delete this?

It seems like it duplicates create_station_kdtree.py

"""

import metro_parts
import kdtree
import csv


class Station():
    def __init__(self, name, coords):

        self.name = name
        self.coords = coords # tuple (lat, long)

    def __getitem__(self, key):
        return self.coords[key]

    def __len__(self):
        return len(self.coords)

    def __str__(self):
        return self.name + " : " + str(self.coords)


class CTAKdTree():

    nodes_lat_long_file = "nodes_with_latlng.txt"

    def __init__(self):
        # Create an empty tree of 2 dimensions for lat,long
        self.tree = kdtree.create(dimensions=2)
        stations_file = open(CTAKdTree.nodes_lat_long_file, "r")

        # Read each station into the kdtree
        for line in stations_file:
            line = line.split(",")
            name = line[0]
            coords = (float(line[1]), float(line[2]))
            self.tree.add(Station(name, coords))

        self.tree = self.tree.rebalance()


    # returns tuple of (station name, coords, dist) for the nearest station
    def nearest(self, lat, lon):
        tup = self.tree.search_nn((lat, lon))
        name = tup[0].data.name
        dist = tup[1]
        return (name, dist)

def main():
    t = CTAKdTree()
    test = (1,2)
    res = t.nearest(test[0], test[1])
    print("Nearest node to " + str(test) + " is:")
    print(res)

if __name__ == "__main__":
    main()
