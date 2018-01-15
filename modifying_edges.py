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
import heapq
from random import shuffle, randint, sample

def delete_one_edge_and_evaluate(graph, test_type=None, x_axis_data=None):
    overall_start_time = time.time()
    graph = deepcopy(graph)
    edge_centralities = nx.edge_betweenness_centrality(graph.G, weight="flow")
    unmodified_alpha_0_score = graph_measure(graph, "activity_and_popularity", alpha=0)
    unmodified_alpha_1_score = graph_measure(graph, "activity_and_popularity", alpha=1)
    unmodified_metro_score = graph_measure(
        graph, "metro_performance", missed_trips=0, modified_edge_dist=0
    )
    print("Finished initialization...", str(time.time() - overall_start_time), "sec")
    
    removal_effects_alpha_0, removal_effects_alpha_1 = [], []
    removal_effects, centralities, edges_in_order = [], [], []
    missed_trips, flows, distances, changed_trips = [], [], [], [] 
    changed_trips_distance, conserved_trips = [], []
    
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
            modified_edge=edge, modified_edge_dist=distance, redistribute_flow=False
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
            
    plot_options = {
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
            "file_name": "metro_performance_",
            "y_on_the_plot": removal_effects
        },
        "activity_and_popularity_0": {
            "title": r"Effect of Removing a Link, $\alpha$ = " + str(0) + " (emphasizes degree over flow)",
            "file_name": "no_redistribution_activity_and_popularity_alpha_" + str(0) + "_",
            "y_on_the_plot": removal_effects_alpha_0
        },
        "activity_and_popularity_1": {
            "title": r"Effect of Removing a Link, $\alpha$ = " + str(1) + " (without re-assigning flow)",
            "file_name": "no_redistribution_activity_and_popularity_alpha_" + str(1) + "_",
            "y_on_the_plot": removal_effects_alpha_1
        }
    }
    
    # x_axis_data=["flows", "centralities", "distances", "num_missed_trips"]
    def helper_make_plots(y=None, title_key=None):
        for this_x_axis_data in x_axis_data:
            make_plot(
                x=plot_options[this_x_axis_data]["x_on_the_plot"], 
                y=plot_options[title_key]["y_on_the_plot"], 
                type_of_plot="scatter",
                ylabel="Percentage Change in Graph Performance", 
                xlabel=plot_options[this_x_axis_data]["xlabel"],
                title=plot_options[title_key]["title"],
                file_name=plot_options[title_key]["file_name"] + this_x_axis_data + ".png"
            )
                
    # helper_make_plots(y=removal_effects, title_key="metro_performance")
    # helper_make_plots(y=removal_effects_alpha_0, title_key="activity_and_popularity_0")
    # helper_make_plots(y=removal_effects_alpha_1, title_key="activity_and_popularity_1")

def add_new_edge(graph, num_edges_to_consider=15, prune_method=None, test_type=None):
    graph = deepcopy(graph)
    
    # Find all possible edges that can be added to the graph 
    possible_new_edges = []
    for node_a in graph.nodes():
        for node_b in graph.nodes():
            if node_a != node_b and not graph.has_edge(edge=(node_a, node_b)):
                possible_new_edges.append((node_a, node_b))
                
    unmodified_metro_score = graph_measure(graph, test_type, missed_trips=0, alpha=1)
    # average_flow = get_typical_attribute_value(graph, attribute_name="flow")
    
    # Choose a random sample from the edges to serve as a benchmark 
    shuffle(possible_new_edges)
    random_edges = sample(possible_new_edges, num_edges_to_consider)
    shuffle(random_edges)
    random_results, best_random_result, flows_random = performance_metric_on_addition_of_edge(
        deepcopy(graph), random_edges, test_type, unmodified_metro_score
    )
    
    if prune_method == "prune_edges_by_score":
        best_n_edges = prune_edges_by_score(
            graph, possible_new_edges, unmodified_metro_score, num_edges_to_consider,
            flow="random"
        )
    elif prune_method == "prune_edges_by_distance_flow_product":
        best_n_edges = prune_edges_by_distance_flow_product(graph, num_edges_to_consider)
    
    pruned_edges = []
    for score, edge, flow in best_n_edges:
        pruned_edges.append(edge)

    shuffle(pruned_edges)
    pruned_edges = sample(possible_new_edges, num_edges_to_consider)
    pruned_edge_results, best_pruned_result, flows = performance_metric_on_addition_of_edge(
        deepcopy(graph), pruned_edges, test_type, unmodified_metro_score
    )
        
    make_plot( 
        y=pruned_edge_results, y2=random_results, type_of_plot="scatter",
        y_annotation=flows, y2_annotation=flows_random,
        ylabel="Percentage Change in Graph Performance", 
        xlabel="Edge Index", legend=["Top Picks After Pruning", "Randomly Picked Edges"],
        title="Comparing Effects on Performance from the Pruned Set of Edges",
        file_name=prune_method + ".png"
    )
    print(best_pruned_result)
    
def performance_metric_on_addition_of_edge(metro_graph_object, edges, test_type, unmodified_metro_score):
    best_candidate = (float("inf")*-1, None)
    record_of_metrics = []
    flows = []
    for i, edge in enumerate(edges):
        distance = metro_graph_object.distance_between_two_nodes(edge[0], edge[1])
        metro_graph_object.add_edge(edge=edge, flow=0, capacity=80000, distance=distance)
        missed, changed_dist, conserved = metro_graph_object.fill_flows_from_mapped_data(
            modified_edge=edge, redistribute_flow=True
        )
        measure = graph_measure(metro_graph_object, test_type, alpha=1, missed_trips=missed)
        measure = ((measure - unmodified_metro_score) / unmodified_metro_score) * (100.0)
        record_of_metrics.append(measure)
        flows.append(metro_graph_object.get_edge_attribute(edge=edge, attribute_name="flow"))
        metro_graph_object.remove_edge(edge=edge)
        if measure > best_candidate[0]:
            best_candidate = (measure, edge)
        if i % 5 == 0: print("Evaluated candidate", i, "score:", measure)
            
    return record_of_metrics, best_candidate, flows
    
def prune_edges_by_score(graph, possible_new_edges, unmodified_metro_score, 
    num_edges_to_consider, flow="random"):
    best_n_candidates = []
    i = 0
    for edge in possible_new_edges:
        if flow == "random":
            flow = randint(1, 60000)
        else:
            flow = flow
        graph.add_edge(edge=edge, flow=flow)
        graph.fill_flows_from_mapped_data(
            modified_edge=edge, modified_edge_dist=1, redistribute_flow=False
        )
        estimated_score = graph_measure(graph, "activity_and_popularity", alpha=1)
        graph.remove_edge(edge=edge)
        maintain_max_heap(best_n_candidates, num_edges_to_consider, (estimated_score, edge, flow))
        i += 1
        if i % 50 == 0: 
            print("Iteration", i, "best champ...:", best_n_candidates[-1])
        # if i == 1000:    
        #     break
        
    return best_n_candidates

def maintain_max_heap(heap_list, max_capacity, new_item):
    if len(heap_list) < max_capacity:
        heapq.heappush(heap_list, new_item)
    elif new_item[0] > heapq.nsmallest(1, heap_list)[0][0]:
        heapq.heappushpop(heap_list, new_item)
    assert(len(heap_list) <= max_capacity)
    # return heap_list   
    
def prune_edges_by_distance_flow_product(graph, num_edges_to_consider):
    journeys = graph.journeys
    best_n_candidates = []
    i = 0
    for journey in journeys:
        # Score = distance of the trip * number of people taking the trip.
        score = graph.distance_between_two_nodes(journey[0], journey[1]) * journeys[journey]
        maintain_max_heap(best_n_candidates, num_edges_to_consider, (score, journey, 0))  
        i += 1
        if i % 5000 == 0: print("Evaluated", i, "possible edges using distance * flow")
        
    print("Found", len(best_n_candidates), "candidates from", len(journeys), "possible edges")  
    return best_n_candidates
    
def get_typical_attribute_value(graph, attribute_name="flow", average="mean"):
    if average == "mean":
        running_sum = 0
        i = 0
        for edge in graph.edges():
            i += 1
            running_sum += graph.get_edge_attribute(edge=edge, attribute_name=attribute_name)
        
        return running_sum / i            

def graph_measure(metro_graph_object, test_type, **kwargs):
    if test_type == "activity_and_popularity":
        alpha = kwargs["alpha"]
        return metro_graph_object.graph_popularity(alpha=alpha) + metro_graph_object.graph_activity(alpha=alpha)
    elif test_type == "metro_performance":
        return metro_graph_object.metro_network_performance(utility_over_cost=10, missed_trips=kwargs["missed_trips"])
    else:
        raise ValueError("Please provide a valid test.")
    

def make_plot(x=None, y=None, xlabel=None, ylabel=None, title=None, 
    type_of_plot=None, file_name=None, **kwargs):
    plt.figure(1)
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
    x2 = None
    
    if x is None:
        x = list(range(1, len(y)+1))
        
    if type_of_plot == "scatter":
        plt.scatter(x, y, c="b")
        if "y2" in kwargs:
            try:
                plt.scatter(x, kwargs["y2"], c="r")
                x2 = x
            except ValueError:
                x2 = list(range(1, len(kwargs["y2"])))
                plt.scatter(x2, kwargs["y2"], c="r")
                
        if "y3" in kwargs:
            plt.scatter(x, kwargs["y3"], c="g")
    else:
        raise ValueError("Please provide a valid type of plot")
    
    if "legend" in kwargs:
        plt.legend(kwargs["legend"], loc="best")
    
    if "y_annotation" in kwargs:
        try:
            for i, (score, edge, flow) in enumerate(kwargs["y_annotation"]):
                plt.annotate(flow, (x[i], y[i]))
        except (ValueError, TypeError):
            for i, flow in enumerate(kwargs["y_annotation"]):
                plt.annotate(flow, (x[i], y[i]))
                
    if "y2_annotation" in kwargs:
        try:
            for i, (score, edge, flow) in enumerate(kwargs["y2_annotation"]):
                plt.annotate(flow, (x2[i], kwargs["y2"][i]))
        except (ValueError, TypeError):
            for i, flow in enumerate(kwargs["y2_annotation"]):
                plt.annotate(flow, (x2[i], kwargs["y2"][i]))
                
    
    if file_name is not None:
        plt.savefig("images/"+file_name, format="png")
        
    plt.show()
    
def main():
    start_time = time.time()
    print("Initializing metro graph...")
    graph = metro_graph()
    print("Done!", str(time.time() - start_time), "sec")
    add_new_edge(
        graph, prune_method="prune_edges_by_distance_flow_product",
        test_type="metro_performance"
    )

if __name__ == "__main__":
    main()
