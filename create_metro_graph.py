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

class metro_graph(nx.classes.digraph.DiGraph):
    
    def __init__(self):
        self.G = nx.DiGraph()
        
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
    
    def add_node(self, node, **kwargs):
        self.G.add_node(node, kwargs)
    
    def store_as_pickle(self):
        output_file = open("metro_graph.pkl",'wb')
        pickle.dump(self.G, output_file)
        output_file.close()
    
    def nodes(self):
        return self.G.nodes()
    
    def edges(self, nodes=None, incoming=False, outgoing=False):
        if incoming and not outgoing:
            return self.G.in_edges(nbunch=nodes)
        elif outgoing and not incoming:
            return self.G.out_edges(nbunch=nodes)
        else:
            return self.G.edges(nbunch=nodes)    
    
    def add_edge(self, edge=None, source_node=None, target_node=None, **kwargs):
        relevant_edge = self._get_relevant_edge(edge, source_node, target_node)
        if not self.has_node(relevant_edge[0]):
            raise ValueError("Node {0} does not exist in the graph".format(relevant_edge[0]))
        if not self.has_node(relevant_edge[1]):
            raise ValueError("Node {0} does not exist in the graph".format(relevant_edge[1]))
        self.G.add_edge(relevant_edge[0], relevant_edge[1], kwargs)
    
    def number_of_nodes(self):
        return nx.number_of_nodes(self.G)
    
    def number_of_edges(self):
        return nx.number_of_edges(self.G)
    
    def neighbors(self, node, predecessors=False, successors=False):
        if predecessors and not successors:
            return self.G.predecessors(node)
        elif successors and not predecessors:
            return self.G.successors(node)
        else:
            return list(nx.all_neighbors(self.G, node))
    
    def add_attribute_to_node(self, node, **kwargs):
        for key in kwargs:
            attribute = {
                node : kwargs[key]
            }
            nx.set_node_attributes(self.G, key, attribute)
        
    def get_node_attribute(self, node, attribute_name="station"):
        return nx.get_node_attributes(self.G, attribute_name)[node]
        
    def has_node(self, node):
        return self.G.has_node(node)
        
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
    
    def has_edge(self, edge=None, source_node=None, target_node=None):
        relevant_edge = self._get_relevant_edge(edge, source_node, target_node)
        return self.G.has_edge(relevant_edge[0], relevant_edge[1])
        
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
    
def main():
    test_graph = metro_graph()
    test_station = "Addison (Brown Line)"
    test_station_2 = "Paulina (Brown Line)"
    print_padding = "{0:60}"
    
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

    for edge in test_graph.edges():
        test_graph.add_attribute_to_edge(edge=edge, flow=random.randint(1, 1000))    
    print(print_padding.format("Testing graph_activity() and node_activity()"), end="... ")    
    print(test_graph.graph_activity(alpha=0.5))
    print(print_padding.format("Testing graph_popularity() and node_popularity()"), end="... ")
    print(test_graph.graph_popularity(alpha=0.5))

if __name__ == "__main__":
    main()
