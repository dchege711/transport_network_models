

import networkx as nx
import matplotlib.pyplot as plt

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
G.add_nodes_from([MetroNode(line.strip()) for line in nodes_file])

# Print the nodes
# for node in G.nodes:
#     print(node)

lines_files = ['brown_line.txt']#, 'blue.txt']
delimiter = ","

for metro_line in lines_files:

    curr_file = open(metro_line, "r")
    elist = []

    for txt_line in curr_file:

        map(str.strip, txt_line.split(delimiter)) 

        # first direction of edge
        elist.extend([(txt_line[i], txt_line[i+1], 0) for i in range(len(txt_line) - 1)])
        # second direction of edge
        elist.extend([(txt_line[i+1], txt_line[i], 0) for i in range(len(txt_line) - 1)])


    G.add_weighted_edges_from(elist)


for e in G.edges_iter():
    print(str(e))
# plt.subplot(121)
# nx.draw(G)
# plt.subplot(122)
# nx.draw(G, pos=nx.circular_layout(G), nodecolor='r', edge_color='b')
# plt.show()




