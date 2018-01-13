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
import numpy as np
import time

def delete_one_edge_and_evaluate(graph):
    graph = deepcopy(graph)
    alpha = 2
    edge_centralities = nx.edge_betweenness_centrality(graph.G, weight="flow")
    unmodified_graph_score = graph_measure(graph, alpha=alpha)
    removal_effects = []
    centralities = []
    edges_in_order = []
    i = 1
    flows = []
    for edge in edge_centralities:
        start_time = time.time()
        # Get an in-order record of the edges and their flows
        edges_in_order.append(edge)
        flow = graph.get_edge_attribute(edge=edge, attribute_name="flow")
        capacity = graph.get_edge_attribute(edge=edge, attribute_name="capacity")
        distance = graph.get_edge_attribute(edge=edge, attribute_name="distance")
        flows.append(flow)
        # Experiment part 1: Remove an edge
        graph.remove_edge(edge=edge)
        graph.fill_flows_from_mapped_data()
        effect = ((graph_measure(graph, alpha=alpha) - unmodified_graph_score)/unmodified_graph_score)*100.0
        removal_effects.append(effect)
        # Experiment part 2: Re-insert the edge so that results are comparable
        centralities.append(edge_centralities[edge])
        graph.add_edge(edge=edge, flow=flow, capacity=capacity, distance=distance)
        end_time = time.time()
        print("Iteration:", i, "duration:", str(end_time - start_time), "seconds\n")
        i += 1
        if i == 10: break
    
    make_plot(
        x=centralities, y=removal_effects, type_of_plot="scatter",
        ylabel="Percentage Change in Graph Activity", 
        xlabel="Betweenness Centrality of the Removed Edge",
        title=r"Effect of Removing a Link ($\alpha$ = " + str(alpha) + " )",
        file_name="centralities_alpha_" + str(alpha) + ".png"
    )
    
    make_plot(
        x=flows, y=removal_effects, type_of_plot="scatter",
        ylabel="Percentage Change in Graph Activity", 
        xlabel="Flow of the Removed Edge",
        title=r"Effect of Removing a Link ($\alpha$ = " + str(alpha) + " )",
        file_name="flow_alpha_" + str(alpha) + ".png"
    )
    
    indexes_in_sorted_list = np.argsort(removal_effects)
    for index in indexes_in_sorted_list[-2:]:
        print(
            "{0:60}".format(str(edges_in_order[index])), 
            "\tcentrality =", "{0:.4f}".format(centralities[index]), 
            "\teffect (%) =", "{0:.4f}".format(removal_effects[index]), 
            "\tflow       =", flows[index]
        )
    for index in indexes_in_sorted_list[:2]:
        print(
            "{0:60}".format(str(edges_in_order[index])), 
            "centrality =", "{0:.4f}".format(centralities[index]), 
            "effect (%) =", "{0:.4f}".format(removal_effects[index]), 
            "flow       =", flows[index]
        )
    print("\nFor reference, the maximum flow on an edge was", np.max(flows), "and the max centrality was", np.max(centralities))
        
    
def graph_measure(graph, alpha=0.5):
    # return graph.graph_popularity(alpha=alpha) + graph.graph_activity(alpha=alpha)
    return graph.metro_network_performance()

def make_plot(x=None, y=None, xlabel=None, ylabel=None, title=None, type_of_plot=None, file_name=None):
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
    
    if file_name is not None:
        plt.savefig("images/"+file_name, format="png")
    plt.show()
    
def main():
    
    graph = metro_graph()
    # graph.randomize_all_flows(1000)
    delete_one_edge_and_evaluate(graph)

if __name__ == "__main__":
    main()
