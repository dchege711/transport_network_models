"""
This script tries to answer one of our research questions:
    * Where is the optimal place of adding a new link?
    * Which link, if deleted, has the greatest impact on the graph?

"""
from copy import deepcopy
from create_metro_graph import metro_graph
from matplotlib import pyplot as plt
from pprint import pprint
import networkx as nx
import operator

def delete_by_betweeness_centrality(graph):
    """
    Remarks:
        * Slow, takes about 6sec to run this. 
        * The plot doesn't show any pattern to it.
        
    """
    graph = deepcopy(graph)
    edge_centralities = nx.edge_betweenness_centrality(graph.G, weight="flow")
    edge_centralities = sorted(edge_centralities.items(), key=operator.itemgetter(1))
    importance_measures = []
    scores = []
    i = 1
    for edge, centrality in edge_centralities:
        flow = graph.get_edge_attribute(edge=edge, attribute_name="flow")
        graph.remove_edge(edge=edge)
        activity = graph.graph_popularity()
        # print(score, activity)
        importance_measures.append(activity)
        scores.append(score)
        graph.add_edge(edge=edge, flow=flow)
        if (i % 10 == 0): print("Iteration:", i, "centrality:", score)
    
    line_plot(
        x=scores, y=importance_measures, 
        ylabel="Graph Activity", xlabel="Betweenness centrality of removed edge",
        title="Removing edges by decreasing betweenness centrality"
    )


def line_plot(x=None, y=None, xlabel=None, ylabel=None, title=None):
    plt.figure(1)
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.plot(x, y, color='b')
    plt.show()
    
def main():
    
    graph = metro_graph()
    graph.randomize_all_edge_weights(1000)
    
    delete_by_betweeness_centrality(graph)

if __name__ == "__main__":
    main()
