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

def delete_by_betweeness_centrality(graph):
    """
    Remarks:
        * Slow, takes about 6sec to run this. 
        * The plot doesn't show any pattern to it.
        
    """
    graph = deepcopy(graph)
    edge_centralities = nx.edge_betweenness_centrality(graph.G, weight="flow")
    importance_measures = []
    centralities = []
    i = 1
    unmodified_graph_score = graph_measure(graph)
    for edge in edge_centralities:
        flow = graph.get_edge_attribute(edge=edge, attribute_name="flow")
        graph.remove_edge(edge=edge)
        importance_measures.append(graph_measure(graph) - unmodified_graph_score)
        centralities.append(edge_centralities[edge])
        graph.add_edge(edge=edge, flow=flow)
        if (i % 20 == 0): print("Iteration:", i, "centrality:", edge_centralities[edge])
        i += 1
    
    make_plot(
        x=centralities, y=importance_measures, type_of_plot="scatter",
        ylabel=r"$\Delta$ in Graph Activity", xlabel="Betweenness centrality of removed edge",
        title="Removing edges by decreasing betweenness centrality"
    )
    
def graph_measure(graph):
    # alpha > 1 gives a higher score to the node with smallest number of outgoing links
    return graph.graph_activity(alpha=0.2)


def make_plot(x=None, y=None, xlabel=None, ylabel=None, title=None, type_of_plot=None):
    plt.figure(1)
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if type_of_plot == "line":
        plt.plot(x, y)
    elif type_of_plot == "scatter":
        plt.scatter(x, y)
    else:
        raise ValueError("Please provide a valid type of plot")
    plt.show()
    
def main():
    
    graph = metro_graph()
    graph.randomize_all_edge_weights(1000)
    
    delete_by_betweeness_centrality(graph)

if __name__ == "__main__":
    main()
