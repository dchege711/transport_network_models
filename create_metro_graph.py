"""
Creates a directed graph with train stations as nodes (and with lat-lng attributes).
Adds unweighted edges between stations that have a direct connection to each other.
Stores the resulting graph in binary format for subsequent processing.

"""

import networkx as nx
import matplotlib.pyplot as plt
from metro_parts import *
import pickle

import utilities as ut

# the digraph of the metro system
G = nx.DiGraph()

# Create a digraph with the nodes from the file containing stations and lat-lng
for line in open(ut.get_path("nodes_with_latlng.txt"), "r"):
    # Each line follows the pattern "station_name    latitude    longitude"
    station_details = line.strip().split(",")
    lat = float(station_details[1])
    lng = float(station_details[2])
    G.add_node(station_details[0], pos=(lng, lat))


# These files were manually compiled. They have station names on a given line
lines_files = [
    'blue.txt', 'brown.txt', 'green.txt', 'orange.txt',
    'pink.txt', 'purple.txt', 'yellow.txt', 'red.txt'
]

# For each pair of adjacent stations, create two links to denote the bidirectional
# nature of railway stations
for metro_line in lines_files:
    curr_file = open(ut.get_path(metro_line), "r")
    elist = []
    for txt_line in curr_file:
        txt_line = txt_line.split(",")
        for i in range(len(txt_line)):
            txt_line[i] = txt_line[i].strip()
        # first direction of edge
        elist.extend([(txt_line[i], txt_line[i+1]) for i in range(len(txt_line) - 1)])
        # second direction of edge
        elist.extend([(txt_line[i+1], txt_line[i]) for i in range(len(txt_line) - 1)])
    G.add_edges_from(elist)

# Store the graph as a pickle file for later references
output_file = open(graph_pickle_file_name,'wb')
pickle.dump(G, output_file)
output_file.close()
