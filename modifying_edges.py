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

def delete_one_edge_and_evaluate(graph, test_type="metro_performance", 
    x_axis_data=["flows"], alpha=2):

    graph = deepcopy(graph)
    edge_centralities = nx.edge_betweenness_centrality(graph.G, weight="flow")
    unmodified_graph_score = graph_measure(graph, test_type, alpha=alpha)
    
    removal_effects, centralities, edges_in_order = [], [], []
    missed_trips, flows, distances = [], [], []
    i = 0
    start_time = time.time()
    for edge in edge_centralities:
        # Get an in-order record of the edges and their flows
        edges_in_order.append(edge)
        flow = graph.get_edge_attribute(edge=edge, attribute_name="flow")
        capacity = graph.get_edge_attribute(edge=edge, attribute_name="capacity")
        distance = graph.get_edge_attribute(edge=edge, attribute_name="distance")
        flows.append(flow)
        distances.append(distance)
        # Experiment part 1: Remove an edge
        graph.remove_edge(edge=edge)
        missed, changed, conserved = graph.fill_flows_from_mapped_data()
        missed_trips.append(missed)
        measure = graph_measure(graph, test_type, alpha=alpha)
        effect = ((measure - unmodified_graph_score)/unmodified_graph_score)*100.0
        removal_effects.append(effect)
        # Experiment part 2: Re-insert the edge so that results are comparable
        centralities.append(edge_centralities[edge])
        graph.add_edge(edge=edge, flow=flow, capacity=capacity, distance=distance)
        
        # Add some logging so that we don't lose hope
        i += 1
        if i % 1 == 0:
            end_time = time.time() 
            print(
                i, "{0:.2f}".format(end_time - start_time), "sec", 
                missed, "missed", changed, "changed", conserved, "conserved"
            )
            start_time = time.time()
        
    plot_options = {
        "flows" : {
            "x_on_the_plot": flows,
            "xlabel": "Flow of the Removed Edge"
        },
        "centralities" : {
            "x_on_the_plot": centralities,
            "xlabel": "Betweenness Centrality of the Removed Edge"
        },
        "num_missed_trips" : {
            "x_on_the_plot": missed_trips,
            "xlabel": "# of Missed Trips Caused by Missing Edge"
        },
        "distances" : {
            "x_on_the_plot": distances,
            "xlabel": "Length of the Removed Edge (km)"
        },
        "metro_performance": {
            "title": "Percentage Effect of Removing a Link",
            "file_name": "metro_performance_"
        },
        "activity_and_popularity": {
            "title": r"Percentage Effect of Removing a Link ($\alpha$ = " + str(alpha) + " )",
            "file_name": "activity_and_popularity_alpha_" + str(alpha) + "_"
        }
    }
    
    for this_x_axis_data in x_axis_data:
        make_plot(
            x=plot_options[this_x_axis_data]["x_on_the_plot"], 
            y=removal_effects, type_of_plot="scatter",
            ylabel="Percentage Change in Graph Performance", 
            xlabel=plot_options[this_x_axis_data]["xlabel"],
            title=plot_options[test_type]["title"],
            file_name=plot_options[test_type]["file_name"] + this_x_axis_data + ".png"
        )
    
    indexes_in_sorted_list = np.argsort(removal_effects)
        
    def print_stats(stats_indexes):
        for index in stats_indexes:
            print(
                "{0:60}".format(str(edges_in_order[index])), 
                " centrality  =", "{0:.4f}".format(centralities[index]),  
                " flow        =", flows[index],
                " length (km) =", "{0:.4f}".format(distances[index]),
                " effect (%)  =", "{0:.4f}".format(removal_effects[index])
            )
    
    print_stats(indexes_in_sorted_list[-2:])
    print_stats(indexes_in_sorted_list[:2])
    print( 
        "\nMaximum flow on an edge was", "{0:,}".format(np.max(flows)), "passengers", 
        "\nMax centrality on an edge was", "{0:.4f}".format(np.max(centralities)),
        "\nMax length of an edge (section) was", "{0:.4f}".format(np.max(distances)), "km"
    )
    
    
    
def graph_measure(graph, test_type, **kwargs):
    if test_type == "activity_and_popularity":
        alpha = kwargs["alpha"]
        return graph.graph_popularity(alpha=alpha) + graph.graph_activity(alpha=alpha)
    elif test_type == "metro_performance":
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
    
    plt.show()
    if file_name is not None:
        plt.savefig("images/"+file_name, format="png")
    
def main():
    graph = metro_graph()
    delete_one_edge_and_evaluate(
        graph, test_type="activity_and_popularity", alpha=0,
        x_axis_data=["flows", "centralities", "distances", "num_missed_trips"]
    )
    # delete_one_edge_and_evaluate(
    #     graph, test_type="metro_performance",
    #     x_axis_data=["flows", "centralities", "distances", "num_missed_trips"]
    # )
    

if __name__ == "__main__":
    main()
