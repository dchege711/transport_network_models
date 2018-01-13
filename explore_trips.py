import utilities as ut
import pickle
from create_metro_graph import metro_graph
import numpy as np

journey_dict_file_name = 'journey_counts.pkl'
input_path = ut.get_path(journey_dict_file_name)
input_file = open(input_path,'rb')
journeys = pickle.load(input_file)
input_file.close()

with_one_space = "California (Blue Line)"
with_two_spaces = "California  (Blue Line)"
one_space, two_space = 0, 0
for journey in journeys:
    if with_one_space in journey:
        one_space += 1
    elif with_two_spaces in journey:
        two_space += 1
print("One space:", one_space, "Two space:", two_space)


# test_graph = metro_graph()
# 
# 
# print(len(journeys), "journeys")
# origin_present = {}
# origin_absent = {}
# dest_present = {}
# dest_absent = {}
# 
# for journey in journeys:
#     a = journey[0]
#     b = journey[1]
#     c = journeys[journey]
#     if test_graph.has_node(a):
#         if a not in origin_present:
#             origin_present[a] = []
#         origin_present[a].append(c)
#     else:
#         if a not in origin_absent:
#             origin_absent[a] = []
#         origin_absent.append(c)
#     if test_graph.has_node(b):
#         if b not in dest_present:
#             dest_present[b] = []
#         dest_present[b].append(c)
#     else:
#         if b not in dest_absent:
#             dest_absent[b] = []
#         dest_absent[b].append(c)
# 
# print("Checking that graph has 'California (Blue Line)' ...", test_graph.has_node('California (Blue Line)'))
# print("Checking that graph has 'California  (Blue Line)'...", test_graph.has_node('California  (Blue Line)'))
# 
# num_zeros = 0
# for origin in origin_present:
#     num_zeros += len(origin_present[origin]) - np.count_nonzero(origin_present[origin])
# 
# print(num_zeros, "journeys have no people on them\n")
