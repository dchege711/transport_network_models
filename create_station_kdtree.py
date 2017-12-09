"""
Creates a K-d Tree using the stations lat-lng coordinates as keys.

"""

import kdtree
import csv
import pickle
from metro_parts import *
import utilities as ut

# Create an empty tree of 2 dimensions for lat,long
tree = kdtree.create(dimensions=2)

stations_file = open(ut.get_path("nodes_with_latlng.txt"), "r")

# Read each station into the kdtree
for line in stations_file:
     line = line.split(",")
     name = line[0]
     coords = (float(line[1]), float(line[2]))
     tree.add(Station(name, coords))

tree = tree.rebalance()
print("Tree is balanced = " + str(tree.is_balanced))

# output_file = open(metro_parts.station_kdtree_file_name,'wb')
# pickle.dump(tree, output_file)
# output_file.close()

# Visualize the Tree
# kdtree.visualize(tree)

# Retrieving the Tree in inorder
# print(list(tree.inorder()))
# Retrieving the Tree in level order
# print(list(kdtree.level_order(tree)))
