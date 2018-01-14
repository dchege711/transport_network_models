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

def delete_one_edge_and_evaluate(graph, test_type=None, 
    x_axis_data=["flows"], alpha=2):
    
    overall_start_time = time.time()
    graph = deepcopy(graph)
    edge_centralities = nx.edge_betweenness_centrality(graph.G, weight="flow")
    unmodified_alpha_0_score = graph_measure(graph, "activity_and_popularity", alpha=0)
    unmodified_alpha_1_score = graph_measure(graph, "activity_and_popularity", alpha=1)
    unmodified_metro_score = graph_measure(
        graph, "metro_performance", missed_trips=0, removed_edge_dist=0
    )
    
    removal_effects_alpha_0, removal_effects_alpha_1 = [], [], []
    removal_effects, centralities, edges_in_order = [], [], []
    missed_trips, flows, distances, changed_trips = [], [], [] 
    changed_trips_distance, conserved_trips = [], [], []
    
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
        missed, changed_dist, conserved = graph.fill_flows_from_mapped_data(
            removed_edge=edge, removed_edge_dist=distance, redistribute_flow=False
        )
        missed_trips.append(missed)
        changed_trips.append(changed_dist[0])
        changed_trips_distance.append(changed_dist[1])
        conserved_trips.append(conserved)
        
        # Run all the experiments back to back because it's faster that way
        measure = graph_measure(graph, "activity_and_popularity", alpha=0)
        effect = ((measure - unmodified_alpha_0_score)/unmodified_alpha_0_score)*100.0
        removal_effects_alpha_0.append(effect)
        measure = graph_measure(graph, "activity_and_popularity", alpha=1)
        effect = ((measure - unmodified_alpha_1_score)/unmodified_alpha_1_score)*100.0
        removal_effects_alpha_1.append(effect)
        measure = graph_measure(graph, "metro_performance", missed_trips=missed)
        effect = ((measure - unmodified_metro_score)/unmodified_metro_score)*100.0
        removal_effects.append(effect)
        
        # Experiment part 2: Re-insert the edge so that results are comparable
        centralities.append(edge_centralities[edge])
        graph.add_edge(edge=edge, flow=0, capacity=capacity, distance=distance)
        
        # Add some logging so that we don't lose hope
        i += 1
        if i == 150:
            break
        if i % 1 == 0:
            end_time = time.time() 
            print(
                "{0:4}".format(i), ": {0:5.2f}".format(end_time - start_time), "sec", 
                "  {0:7}".format("{0:,}".format(missed)), "missed", 
                "  {0:10}".format("{0:.2f}".format(changed_dist)), "changed_dist", 
                "  {0:7}".format("{0:,}".format(conserved)), "conserved"
            )
            start_time = time.time()
            
    end_time = time.time()
    print("\nSimulation took", "{0:5.2f}".format(end_time - overall_start_time), "seconds\n")
        
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
            "title": "Effect on Utility/Cost Analysis of Removing a Link",
            "file_name": "metro_performance_"
        },
        "activity_and_popularity_0": {
            "title": r"Effect of Removing a Link, $\alpha$ = " + str(0) + " (emphasizes degree over flow)",
            "file_name": "activity_and_popularity_alpha_" + str(0) + "_"
        },
        "activity_and_popularity_1": {
            "title": r"Effect of Removing a Link, $\alpha$ = " + str(1) + " (emphasizes flow over degree)",
            "file_name": "activity_and_popularity_alpha_" + str(1) + "_"
        }
    }
    
    def helper_make_plots(y=None, title_key=None):
        for this_x_axis_data in x_axis_data:
            make_plot(
                x=plot_options[this_x_axis_data]["x_on_the_plot"], 
                y=removal_effects, type_of_plot="scatter",
                ylabel="Percentage Change in Graph Performance", 
                xlabel=plot_options[this_x_axis_data]["xlabel"],
                title=plot_options[title_key]["title"],
                file_name=plot_options[title_key]["file_name"] + this_x_axis_data + ".png"
            )
    
    make_plot(
        x=centralities, 
        y=missed_trips, type_of_plot="scatter",
        ylabel="# of Trips That Became Infeasible", 
        xlabel="Centrality of Removed Edge",
        title="Effect of the Centrality on the # of Infeasible Trips",
        file_name="infeasible_trips_against_centrality.png"
    )
    
    make_plot(
        x=centralities, 
        y=changed_trips_distance, type_of_plot="scatter",
        ylabel="Change in Total Distance Travelled (km)", 
        xlabel="Centrality of Removed Edge",
        title="Effect of the Centrality on the Distance Travelled",
        file_name="changed_trips_against_centrality.png"
    )
    
    # helper_make_plots(y=removal_effects, title_key="metro_performance")
    # helper_make_plots(y=removal_effects_alpha_0, title_key="activity_and_popularity_0")
    # helper_make_plots(y=removal_effects_alpha_1, title_key="activity_and_popularity_1")
    
    indexes_in_sorted_list = np.argsort(removal_effects)
        
    def print_stats(stats_indexes):
        for index in stats_indexes:
            print(
                "{0:60}".format(str(edges_in_order[index])), 
                " centrality =", "{0:.4f}".format(centralities[index]),  
                " flow =", flows[index],
                " length (km) =", "{0:.4f}".format(distances[index]),
                " effect (%) =", "{0:.4f}".format(removal_effects[index])
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
        return graph.metro_network_performance(utility_over_cost=10, missed_trips=kwargs["missed_trips"])

def make_plot(x=None, y=None, xlabel=None, ylabel=None, title=None, 
    type_of_plot=None, file_name=None, **kwargs):
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if type_of_plot == "line":
        plt.plot(x, y)
    elif type_of_plot == "scatter":
        plt.scatter(x, y, c="b")
        if "y2" in kwargs:
            plt.scatter(x, kwargs["y2"], c="r")
        if "y3" in kwargs:
            plt.scatter(x, kwargs["y3"], c="g")
    else:
        raise ValueError("Please provide a valid type of plot")
    
    if "legend" in kwargs:
        plt.legend(kwargs["legend"], loc="best")
    
    if file_name is not None:
        plt.savefig("images/"+file_name, format="png")
        
    plt.show()
    
def main():
    graph = metro_graph()
    delete_one_edge_and_evaluate(
        graph, test_type="activity_and_popularity", alpha=1,
        x_axis_data=["flows", "centralities", "distances", "num_missed_trips"]
    )
    # delete_one_edge_and_evaluate(
    #     graph, test_type="metro_performance",
    #     x_axis_data=["flows", "centralities", "distances", "num_missed_trips"]
    # )
    

if __name__ == "__main__":
    main()
