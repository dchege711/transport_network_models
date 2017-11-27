

import networkx as nx
import matplotlib.pyplot as plt

import pickle


class MetroNode():

    def __init__(self, name):

        self.name = name

    def __str__(self):

        return self.name

    def __hash__(self):

        return hash(str(self.name))

    def __eq__(self, other):
        return self.name == other.name

class MetroEdge():

    def __init__(self, daily_flow = None, weekly_flow = None):

        self.daily_flow = daily_flow
        self.weekly_flow = weekly_flow

    def setDaily(self, val):
        self.daily_flow = val

    def setWeekly(self, val):
        self.weekly_flow = val



G = nx.DiGraph()

# Create a digraph with the nodes from the node file
nodes_file_name = "nodes.txt"
nodes_file = open(nodes_file_name, "r")

name_index = 0
lat_index = 1
lng_index = 2

for line in nodes_file:
    station_details = line.strip().split(",")
    lat = float(station_details[lat_index])
    lng = float(station_details[lng_index])
    G.add_node(station_details[name_index], pos=(lat, lng))

# G.add_nodes_from(['Paulina','Clinton','Kedzie'])

# Print the nodes
# for node in G.nodes:
#     print(node, end = ", ")

lines_files = ['blue.txt', 'brown.txt', 'green.txt', 'orange.txt', 'pink.txt', 'purple.txt', 'yellow.txt', 'red.txt']
delimiter = ","

for metro_line in lines_files:

    curr_file = open(metro_line, "r")
    elist = []

    for txt_line in curr_file:
        # print("txt_line before = \n\n", str(txt_line))

        txt_line = txt_line.split(delimiter)

        for i in range(len(txt_line)):
            txt_line[i] = txt_line[i].strip()

        # print("txt_line after = \n\n", str(txt_line))

        # first direction of edge
        elist.extend([(txt_line[i], txt_line[i+1]) for i in range(len(txt_line) - 1)])
        # second direction of edge
        elist.extend([(txt_line[i+1], txt_line[i]) for i in range(len(txt_line) - 1)])


    G.add_edges_from(elist)


graph_pickle_file_name = "metro_graph.pkl"

output_file = open(graph_pickle_file_name,'wb')
pickle.dump(G, output_file)
output_file.close()

#Print the edges to terminal
# for e in G.edges:
#     print(e)
