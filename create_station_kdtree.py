"""
create_station_kdtree.py

Creates a K-d Tree using the stations lat-lng coordinates as keys.

"""

import kdtree
import pickle
import metro_parts
import utilities as ut

# Create an empty tree of 2 dimensions for lat,long
tree = kdtree.create(dimensions=2)
stations_file = open(ut.get_path("nodes_with_latlng_updated.txt"), "r")

# Read each station into the kdtree
for line in stations_file:

    station_details = line.strip().split("\t")
    lat_lng = station_details[1].split(",")
    lat = float(lat_lng[0])
    lng = float(lat_lng[1])
    coords = (lat, lng)
    name = station_details[0]
    tree.add(metro_parts.Station(name, coords))    # Station is a class in metro_parts

tree = tree.rebalance()
print("Created a", tree.dimensions, "- d tree")

output_file = open(metro_parts.station_kdtree_file_name, 'wb')
pickle.dump(tree, output_file)
output_file.close()
