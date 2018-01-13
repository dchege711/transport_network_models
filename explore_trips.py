import utilities as ut
import pickle
from create_metro_graph import metro_graph
import numpy as np

journey_dict_file_name = 'journey_counts.pkl'
input_path = ut.get_path(journey_dict_file_name)
input_file = open(input_path,'rb')
journeys = pickle.load(input_file)
input_file.close()

test_graph = metro_graph()


print(len(journeys), "journeys")
origin_present = {}
origin_absent = {}
dest_present = {}
dest_absent = {}

for journey in journeys:
    a = journey[0]
    b = journey[1]
    c = journeys[journey]
    if test_graph.has_node(a):
        if a not in origin_present:
            origin_present[a] = []
        origin_present[a].append(c)
    else:
        if a not in origin_absent:
            origin_absent[a] = []
        origin_absent[a].append(c)
    if test_graph.has_node(b):
        if b not in dest_present:
            dest_present[b] = []
        dest_present[b].append(c)
    else:
        if b not in dest_absent:
            dest_absent[b] = []
        dest_absent[b].append(c)

print("Checking that graph has 'California (Blue Line)' ...", test_graph.has_node('California (Blue Line)'))
print("Checking that graph has 'California  (Blue Line)'...", test_graph.has_node('California  (Blue Line)'))

num_zeros = 0
for origin in origin_present:
    num_zeros += len(origin_present[origin]) - np.count_nonzero(origin_present[origin])

print(num_zeros, "journeys have no people on them\n")
