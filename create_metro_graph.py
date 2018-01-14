"""
create_metro_graph.py

Creates a directed graph with train stations as nodes, with lat-lng attributes.
Adds unweighted edges between stations that have a direct connection.
Stores the resulting graph in binary format for subsequent processing.

"""
import networkx as nx
from metro_parts import Station, MetroEdge
import pickle
import utilities as ut
import sys
from pprint import pprint
import random
import time

class metro_graph():
    
    def __init__(self):
        self.G = nx.DiGraph()
        # SAM
        # Expecting a dict with keys as a (origin_station, destination_station)
        # and the value being how many people are taking that trip.
        journey_dict_file_name = 'journey_counts.pkl'
        input_path = ut.get_path(journey_dict_file_name)
        input_file = open(input_path,'rb')
        self.journeys = pickle.load(input_file)
        input_file.close()
        
        # Remove the trips that have no passengers
        journeys_to_pop = []
        for journey in self.journeys:
            if self.journeys[journey] == 0:
                journeys_to_pop.append(journey)
        for journey in journeys_to_pop:
            self.journeys.pop(journey) 
        
        # Add the stations as nodes
        for line in open(ut.get_path("nodes_with_latlng_updated.txt"), "r"):
            station_details = line.strip().split("\t")
            lat_lng = station_details[1].split(",")
            station = Station(station_details[0], lat_lng)
            self.G.add_node(station_details[0], station=station)
            
        # Link up the stations
        lines_files = [
            'blue.txt', 'brown.txt', 'green.txt', 'orange.txt',
            'yellow.txt','pink.txt', 'purple.txt','red.txt'
        ]
        for metro_line in lines_files:
            curr_file = open(ut.get_path(metro_line), "r")
            elist = []
            stations = []
            for txt_line in curr_file:
                stations.append(txt_line.strip())
            # first direction of edge
            elist.extend([(stations[i], stations[i+1]) for i in range(len(stations) - 1)])
            # second direction of edge
            elist.extend([(stations[i+1], stations[i]) for i in range(len(stations) - 1)])

            self.G.add_edges_from(elist)
            
        # self.store_as_pickle()
        self._set_distances_as_edge_attributes()
        
        # Cache the routes followed by each journey since fill_flows_from_mapped_data()
        # has poor performance (~50 seconds per run)
        self.previous_path_for_journeys = {}
        self.previous_path_lengths_for_journeys = {}
        for journey in self.journeys:
            self.previous_path_for_journeys[journey] = []
            self.previous_path_lengths_for_journeys[journey] = []
        
        # Set the default values for the edges
        for edge in self.edges():
            self.add_attribute_to_edge(edge=edge, capacity=80000, flow=0)
        
        self.num_total_trips = 0
        results = self.fill_flows_from_mapped_data(cache_result=True) 
        assert results[0] == 0, "Expected 0 missed trips. Received {0}".format(results[0])
    
    def add_node(self, node, **kwargs):
        self.G.add_node(node, kwargs)
    
    def store_as_pickle(self):
        output_file = open("metro_graph.pkl",'wb')
        pickle.dump(self.G, output_file)
        output_file.close()
    
    def nodes(self):
        return self.G.nodes()
    
    def remove_node(self, node):
        self.G.remove_node(node)
        
    def has_node(self, node):
        return self.G.has_node(node)
    
    def number_of_nodes(self):
        return nx.number_of_nodes(self.G)
    
    def get_node_attribute(self, node, attribute_name="station"):
        return nx.get_node_attributes(self.G, attribute_name)[node]
    
    def add_attribute_to_node(self, node, **kwargs):
        for key in kwargs:
            attribute = {
                node : kwargs[key]
            }
            nx.set_node_attributes(self.G, key, attribute)
            
    def neighbors(self, node, predecessors=False, successors=False):
        if predecessors and not successors:
            return self.G.predecessors(node)
        elif successors and not predecessors:
            return self.G.successors(node)
        else:
            return list(nx.all_neighbors(self.G, node))
    
    def edges(self, nodes=None, incoming=False, outgoing=False):
        if incoming and not outgoing:
            return self.G.in_edges(nbunch=nodes)
        elif outgoing and not incoming:
            return self.G.out_edges(nbunch=nodes)
        else:
            return self.G.edges(nbunch=nodes) 
        
    def _set_distances_as_edge_attributes(self):
        # Possible improvement: a.dist(b) == b.dist(a), so no need to recompute 
        for edge in self.edges():
            station_a = self.get_node_attribute(edge[0], attribute_name="station")
            station_b = self.get_node_attribute(edge[1], attribute_name="station")
            self.add_attribute_to_edge(edge=edge, distance=station_a.distance_to(station_b))   
    
    def add_edge(self, edge=None, source_node=None, target_node=None, **kwargs):
        relevant_edge = self._get_relevant_edge(edge, source_node, target_node)
        if not self.has_node(relevant_edge[0]):
            raise ValueError("Node {0} does not exist in the graph".format(relevant_edge[0]))
        if not self.has_node(relevant_edge[1]):
            raise ValueError("Node {0} does not exist in the graph".format(relevant_edge[1]))
        self.G.add_edge(relevant_edge[0], relevant_edge[1], kwargs)
    
    def remove_edge(self, edge=None, source_node=None, target_node=None):
        relevant_edge = self._get_relevant_edge(edge, source_node, target_node)
        self.G.remove_edge(relevant_edge[0], relevant_edge[1])
    
    def number_of_edges(self):
        return nx.number_of_edges(self.G)
    
    def has_edge(self, edge=None, source_node=None, target_node=None):
        relevant_edge = self._get_relevant_edge(edge, source_node, target_node)
        return self.G.has_edge(relevant_edge[0], relevant_edge[1])
    
    def randomize_all_flows(self, max_n, edge_attribute="flow"):
        if edge_attribute == "flow":
            for edge in self.edges():
                self.add_attribute_to_edge(edge=edge, flow=random.randint(1, max_n))
                
    def fill_flows_from_mapped_data(self, removed_edge=None, removed_edge_dist=None, cache_result=False):
        # The removed edge may have caused the shortest paths to change
        # The change is measured against the initial complete graph with all edges
        all_shortest_paths = nx.shortest_path(self.G, weight="distance")
        all_shortest_paths_lengths = nx.shortest_path_length(self.G, weight="distance")
        
        # Investigate how the changed paths have affected the flow
        num_missed_trips, changed_trips_distance, num_conserved_trips, num_changed_trips = 0, 0, 0, 0
        for journey in self.journeys:
            flow = self.journeys[journey]
            try:
                # If this doesn't lead to an exception, then the journey is still feasible
                shortest_path = all_shortest_paths[journey[0]][journey[1]]
                shortest_path_length = all_shortest_paths_lengths[journey[0]][journey[1]]
                
                # If this journey still follows the original path, note that down, and then skip
                if shortest_path == self.previous_path_for_journeys[journey]:
                    num_conserved_trips += flow
                    continue
                
                else:
                    # The journey has a new path... 
                    # ... add the flow in this journey to the new shortest path
                    for i in range(len(shortest_path) - 1):
                        edge = (shortest_path[i], shortest_path[i+1])
                        self._helper_for_adjusting_flow(edge, flow)
                        
                    # ... subtract the flow of this journey from its previous shortest path
                    previous_shortest_path = self.previous_path_for_journeys[journey]
                    negated_flow = flow * -1
                    for i in range(len(previous_shortest_path) - 1):
                        edge = (previous_shortest_path[i], previous_shortest_path[i+1])
                        if edge == removed_edge:
                            continue
                        self._helper_for_adjusting_flow(edge, negated_flow)
                        
                    # If we wish to store these as the default values, then do so
                    if cache_result:
                        self.previous_path_for_journeys[journey] = shortest_path
                        self.previous_path_lengths_for_journeys[journey] = shortest_path_length
                        
                    # Note how much the distance has changed for this journey 
                    previous_shortest_path_length = self.previous_path_lengths_for_journeys[journey]
                    num_changed_trips += flow
                    changed_trips_distance += previous_shortest_path_length * flow
                    
            except Exception as e:
                # For all the currently infeasible trips
                num_missed_trips += flow
        
        # Add a sanity check
        total_trips = num_missed_trips + num_changed_trips + num_conserved_trips
        if cache_result:
            self.num_total_trips = total_trips
        else:
            error_msg = "Expected {0} trips. Got {1} trips".format(self.num_total_trips, total_trips)
            assert self.num_total_trips == total_trips, error_msg
        
        return num_missed_trips, (num_changed_trips, changed_trips_distance), num_conserved_trips
    
    def _helper_for_adjusting_flow(self, edge, delta_flow):
        temp = self.get_edge_attribute(
            edge=edge, 
            attribute_name="flow"
        )
        self.add_attribute_to_edge(
            edge=edge,
            flow=temp + delta_flow
        )
        
    def add_attribute_to_edge(self, edge=None, source_node=None, target_node=None, **kwargs):
        relevant_edge = self._get_relevant_edge(edge, source_node, target_node)
        for key in kwargs:
            attribute = {
                relevant_edge : kwargs[key]
            }
            nx.set_edge_attributes(self.G, key, attribute)
        
    def get_edge_attribute(self, edge=None, source_node=None, target_node=None, attribute_name="flow"):
        relevant_edge = self._get_relevant_edge(edge, source_node, target_node)
        return nx.get_edge_attributes(self.G, attribute_name)[relevant_edge]
    
    def _get_relevant_edge(self, edge, source_node, target_node):
        if edge is not None:
            return edge 
        elif source_node is not None and target_node is not None:
            return (source_node, target_node)
        else:
            raise ValueError("Please provide either an edge, or a source_node/target_node combo")
    
    def graph_activity(self, alpha=1, edge_attribute="flow"):
        running_sum = 0
        for node in self.nodes():
            running_sum += self.node_activity(node, alpha=alpha, edge_attribute=edge_attribute)
        return running_sum
    
    def node_activity(self, node, alpha=1, edge_attribute="flow"):
        outward_edges = self.edges(nodes=node, outgoing=True)
        return self._sum_weights_to_power_alpha(alpha, outward_edges, edge_attribute)
        
    def _sum_weights_to_power_alpha(self, alpha, edges, edge_attribute):
        running_sum = 0
        num_edges = len(edges)
        for edge in edges:
            running_sum += self.get_edge_attribute(edge=edge, attribute_name=edge_attribute)
        try:
            return num_edges * ((running_sum / num_edges) ** alpha)
        except ZeroDivisionError:
            return 0
        
    def graph_popularity(self, alpha=1, edge_attribute="flow"):
        running_sum = 0
        for node in self.nodes():
            running_sum += self.node_popularity(node, alpha=alpha, edge_attribute=edge_attribute)
        return running_sum
    
    def node_popularity(self, node, alpha=1, edge_attribute="flow"):
        inward_edges = self.edges(nodes=node, incoming=True)
        return self._sum_weights_to_power_alpha(alpha, inward_edges, edge_attribute)
    
    def metro_network_performance(self, cost_per_unit_distance=10, utility_over_cost=2, missed_trips=0):
        """
        Rationale:
        1. Reward people getting to destinations through shorter routes 
        2. Penalize the existence of longer routes in the graph 
        3. Penalize empty cabins or congested cabins
        4. Add extra penalty for passengers that can't take the train whatsoever
        
        """
        running_sum = 0
        for edge in self.edges():
            distance = self.get_edge_attribute(edge=edge, attribute_name="distance")
            flow = self.get_edge_attribute(edge=edge, attribute_name="flow")
            capacity = self.get_edge_attribute(edge=edge, attribute_name="capacity")
            if flow <= capacity:
                inefficiency = capacity - flow 
            else:
                inefficiency = flow - capacity
                if inefficiency > capacity * 0.4:
                    inefficiency = inefficiency * 2
            
            utility = (flow * distance) * utility_over_cost
            cost = (distance * cost_per_unit_distance + inefficiency) / utility_over_cost
            running_sum += utility - cost
            
        return running_sum - (missed_trips * utility_over_cost)
            
    
def main():

    test_graph = metro_graph()
    test_station = "Addison (Brown Line)"
    test_station_2 = "Paulina (Brown Line)"
    print_padding = "{0:65}"
    
    print(print_padding.format("Testing add_node(), has_node() and number_of_nodes()"), end="... ")
    new_node_1 = "North Pole"
    assert (test_graph.has_node(new_node_1) == False)
    num_nodes = test_graph.number_of_nodes()
    test_graph.add_node(
        new_node_1, station=Station(new_node_1, [90, 0]),
        new_attribute_2="new_attribute_2"
    )
    assert (test_graph.number_of_nodes() == num_nodes + 1)
    print("passed!")
    
    print(print_padding.format("Testing add_attribute_to_node() and get_node_attribute()"), end="... ")
    test_graph.add_attribute_to_node(new_node_1, new_attribute_3="new_attribute_3")
    fetch_attr = test_graph.get_node_attribute(new_node_1, attribute_name="new_attribute_2")
    assert (fetch_attr == "new_attribute_2")
    fetch_attr = test_graph.get_node_attribute(new_node_1, attribute_name="new_attribute_3")
    assert (fetch_attr == "new_attribute_3")
    try:
        test_graph.add_attribute_to_node("This node doesn't exist", flow=5000)
        print("failed!")
    except KeyError:
        print("passed!")
    
    print(print_padding.format("Testing add_edge(), has_edge() & number_of_edges()"), end="... ")
    new_node_2 = "South Pole"
    num_edges = test_graph.number_of_edges()
    new_edge = (new_node_1, new_node_2)
    test_graph.add_node(new_node_2, station=Station(new_node_2, [-90, 0]))
    test_graph.add_edge(edge=new_edge, flow=5000)
    assert (test_graph.number_of_edges() == num_edges + 1)
    non_existent_edge = (new_node_2, new_node_1)
    assert(test_graph.has_edge(edge=non_existent_edge) == False)
    test_graph.remove_edge(edge=new_edge)
    assert(test_graph.number_of_edges() == num_edges)
    test_graph.add_edge(edge=new_edge, flow=5000)
    print("passed!")
    
    print(print_padding.format("Testing add_attribute_to_edge() and get_edge_attribute()"), end="... ")
    fetch_attr = test_graph.get_edge_attribute(edge=new_edge, attribute_name="flow")
    assert(fetch_attr == 5000)
    test_graph.add_attribute_to_edge(edge=new_edge, flow=6000)
    fetch_attr = test_graph.get_edge_attribute(edge=new_edge, attribute_name="flow")
    assert(fetch_attr == 6000)
    try:
        test_graph.add_attribute_to_edge(edge=non_existent_edge, flow=5000)
        print("failed!")
    except KeyError:
        print("passed!")

    # test_graph.randomize_all_flows(10)
    print(print_padding.format("Testing graph_activity() and node_activity()"), end="... ")    
    print(test_graph.graph_activity(alpha=0.5))
    print(print_padding.format("Testing graph_popularity() and node_popularity()"), end="... ")
    print(test_graph.graph_popularity(alpha=0.5))


if __name__ == "__main__":
    main()
