

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

for line in nodes_file:
    G.add_node(line.strip())

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



#Print the edges to terminal
# for e in G.edges:
#     print(e)

# Drawing the graph
options = {
        'node_color': 'r',
        'node_size': 30,
        'width': 2,
        'with_labels': True,
        'nodecolor' :'r',
        'arrows' : True,
        'font_size' : 10,
        'font_color' : 'black',
        'linewidths' : 0.5,
     }


pos = nx.spring_layout(G, k=0.05, iterations=20, scale = 2.0)

# plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')

nx.draw(G, pos, **options)


# plt.subplot(122)
# nx.draw(G, pos=nx.circular_layout(G), nodecolor='r', edge_color='b')
plt.show()




