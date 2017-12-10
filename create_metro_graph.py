"""
create_metro_graph.py

Creates a directed graph with train stations as nodes, with lat-lng attributes.
Adds unweighted edges between stations that have a direct connection.
Stores the resulting graph in binary format for subsequent processing.

"""
import networkx as nx
from metro_parts import *
import pickle
import utilities as ut
import sys

# Create a digraph with the nodes from the file containing stations and lat-lng
G = nx.DiGraph()
for line in open(ut.get_path("nodes_with_latlng_updated.txt"), "r"):
    # Each line follows the pattern "station_name    latitude    longitude"
    station_details = line.strip().split("\t")
    lat_lng = station_details[1].split(",")
    lat = float(lat_lng[0])
    lng = float(lat_lng[1])
    G.add_node(station_details[0], pos=(lng, lat))
    print(station_details[0], " -- ", lat, "--", lng)

# sys.exit()


# These files were manually compiled. They have station names on a given line
lines_files = [
    'blue.txt', 'brown.txt', 'green.txt', 'orange.txt',
  'yellow.txt','pink.txt', 'purple.txt','red.txt'
]
#   

# For each pair of adjacent stations, create two links for bidirectionality
for metro_line in lines_files:
    curr_file = open(ut.get_path(metro_line), "r")
    elist = []
    stations = []
    for txt_line in curr_file:
        stations.append(txt_line.strip())
    # first direction of edge
    elist.extend([(stations[i], stations[i+1]) for i in range(len(stations) - 1)])
    # second direction of edge
    elist.extend([(stations[i+1], stations[i]) for i in range(len(stations) - 1)])

    G.add_edges_from(elist)

# Store the graph as a pickle file for later references
output_file = open(graph_pickle_file_name,'wb')
pickle.dump(G, output_file)
output_file.close()
