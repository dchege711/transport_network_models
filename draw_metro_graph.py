"""
draw_metro_graph.py

Plots a visualization of the transport graph. Uses the lat-lng data
to place the nodes appropriately.

"""

import networkx as nx
import matplotlib.pyplot as plt

import metro_parts
import pickle

# Read in the metro graph G from the pickle file
input_file = open(metro_parts.graph_pickle_file_name,'rb')
G = pickle.load(input_file)
input_file.close()

# Drawing the graph
options = {
    'node_color': 'r',
    'node_size': 30,
    'width': 2,
    'with_labels': True,
    'nodecolor' :'r',
    'edge_color' : 'c',
    'arrows' : False,
    'font_size' : 4,
    'font_color' : 'black',
    'linewidths' : 0.01,

}
nx.draw(G, nx.get_node_attributes(G, 'pos'), **options)
plt.show()
