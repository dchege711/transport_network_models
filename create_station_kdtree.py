

import kdtree
import csv
import pickle
import metro_parts
import utilities as ut

station_kd_tree_file = ut.get_path("station_kdtree.pkl")

class Station():
     def __init__(self, name, coords):

          self.name = name
          self.coords = coords # tuple (lat, long)

     def __getitem__(self, key):
          return self.coords[key]

     def __len__(self):
          return len(coords)

     def __str__(self):
          return self.name + " : " + str(self.coords)


# Create an empty tree of 2 dimensions for lat,long
tree = kdtree.create(dimensions=2)

nodes_lat_long_file = "nodes_with_latlng.txt"
stations_file = open(nodes_lat_long_file, "r")

# Read each station into the kdtree
for line in stations_file:

     line = line.split(",")
     name = line[0]
     coords = (float(line[1]), float(line[2]))
     tree.add(Station(name, coords))
     #print(tree.is_balanced)

tree = tree.rebalance()
print("Tree is balanced = " + str(tree.is_balanced))

output_file = open(metro_parts.station_kdtree_file_name,'wb')
pickle.dump(tree, output_file)
output_file.close()


# Visualize the Tree
# kdtree.visualize(tree)



# Retrieving the Tree in inorder
# print(list(tree.inorder()))
# Retrieving the Tree in level order
# print(list(kdtree.level_order(tree)))
