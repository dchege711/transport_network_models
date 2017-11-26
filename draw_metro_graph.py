

import networkx as nx
import matplotlib.pyplot as plt

import pickle


# Read in the metro graph G from the pickle file
graph_pickle_file_name = "metro_graph.pkl"
input_file = open(graph_pickle_file_name,'rb')
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
        'font_size' : 10,
        'font_color' : 'black',
        'linewidths' : 0.01,
     }


pos = nx.spring_layout(G, k=0.15, iterations=50, scale = 3.0)

# plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')

nx.draw(G, pos, **options)


# plt.subplot(122)
# nx.draw(G, pos=nx.circular_layout(G), nodecolor='r', edge_color='b')
plt.show()