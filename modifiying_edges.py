"""
This script tries to answer one of our research questions:
    * Where is the optimal place of adding a new link?
    * Which link, if deleted, has the greatest impact on the graph?

"""
from copy import deepcopy
from create_metro_graph import metro_graph
from pprint import pprint
# import networkx as nx

def delete_by_betweeness_centrality(graph):
    # betweeness_centralities = nx.edge_betweenness_centrality(graph.G, weight="flow")
    betweeness_centralities = graph.edge_betweenness_centrality(weight="flow", k=2)
    pprint(betweeness_centralities)

def main():
    
    graph = metro_graph()
    graph.randomize_all_edge_weights(1000)
    
    delete_by_betweeness_centrality(graph)

if __name__ == "__main__":
    main()
