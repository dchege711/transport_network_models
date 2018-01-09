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
            
        self.store_as_pickle()
    
    def store_as_pickle(self):
        output_file = open("metro_graph.pkl",'wb')
        pickle.dump(self.G, output_file)
        output_file.close()
    
    def nodes(self):
        return nx.nodes(self.G)
    
    def number_of_nodes(self):
        return nx.number_of_nodes(self.G)
    
    def all_neighbors(self, node):
        return list(nx.all_neighbors(self.G, node))
    
    def outgoing_edges(self, nodes):
        return nx.edges(self.G, nbunch=nodes)
    
    def add_attribute_to_node(self, node, key_val_pairs):
        try:
            for key in key_val_pairs.keys():
                self.G.nodes[node][key] = key_val_pairs[key]
        except:
            raise ValueError("{0} does not exist in the graph".format(node))
        
    def get_node_attribute(self, node, attribute_name="station"):
        try:
            return nx.get_node_attributes(self.G, attribute_name)[node]
        except:
            raise KeyError(
                "Invalid attribute name. Try 'station'"
            )
        
    def add_attribute_to_edge(self, source_node, target_node, key_val_pairs):
        try:
            for key in key_val_pairs.keys():
                self.G.edges[source_node, target_node][key] = key_val_pairs[key]
        except:
            raise ValueError("{0} does not exist in the graph".format(node))
        
    def get_edge_attribute(self, source_node, target_node, key=None):
        if key is None:
            return self.G.edges[source_node, target_node]
        else:
            try:
                return self.G.edges[source_node, target_node][key]
            except KeyError:
                raise KeyError(
                    "Invalid key. Try {0}".format(self.G[source_node, target_node].keys())
                )
            
    def graph_popularity(self, alpha=1):
        running_sum = 0
        for node in self.G.nodes:
            running_sum += self.node_popularity(node, alpha=alpha)
        return running_sum
    
    def node_popularity(self, node, alpha=1, weight_name="density"):
        outward_edges = self.outgoing_edges(node)
        num_outgoing_edges = len(outward_edges)
        sum_outgoing_weights = 0
        for edge in outward_edges:
            sum_outgoing_weights += read_edge_attributes(edge, key=weight_name)
        return num_outgoing_edges * ((sum_outgoing_weights / num_outgoing_edges) ** alpha)        
    
def main():
    test_graph = metro_graph()
    test_station = "Addison (Brown Line)"
    
    nodes = test_graph.nodes()
    print("The graph has", test_graph.number_of_nodes(), "stations, e.g.", nodes[0])
    
    print("\n{0}'s neighbors are:".format(test_station))
    pprint(test_graph.all_neighbors(test_station))
        
    print("\n{0}'s outgoing links are:".format(test_station))
    pprint(test_graph.outgoing_edges(test_station))
    
    print("\n{0}'s attributes are:".format(test_station))
    pprint(test_graph.get_node_attribute(test_station))
    
    

if __name__ == "__main__":
    main()
    
     
# # Create a digraph with the nodes from the file containing stations and lat-lng
# G = nx.DiGraph()
# for line in open(ut.get_path("nodes_with_latlng_updated.txt"), "r"):
#     # Each line follows the pattern "station_name    latitude    longitude"
#     station_details = line.strip().split("\t")
#     lat_lng = station_details[1].split(",")
#     lat = float(lat_lng[0])
#     lng = float(lat_lng[1])
#     G.add_node(station_details[0], pos=(lng, lat))
#     print(station_details[0], " -- ", lat, "--", lng)
# 
# # These files were manually compiled. They have station names on a given line
# lines_files = [
#     'blue.txt', 'brown.txt', 'green.txt', 'orange.txt',
#   'yellow.txt','pink.txt', 'purple.txt','red.txt'
# ]
# #   
# 
# # For each pair of adjacent stations, create two links for bidirectionality
# for metro_line in lines_files:
#     curr_file = open(ut.get_path(metro_line), "r")
#     elist = []
#     stations = []
#     for txt_line in curr_file:
#         stations.append(txt_line.strip())
#     # first direction of edge
#     elist.extend([(stations[i], stations[i+1]) for i in range(len(stations) - 1)])
#     # second direction of edge
#     elist.extend([(stations[i+1], stations[i]) for i in range(len(stations) - 1)])
# 
#     G.add_edges_from(elist)
# 
# # Store the graph as a pickle file for later references
# output_file = open(graph_pickle_file_name,'wb')
# pickle.dump(G, output_file)
# output_file.close()
