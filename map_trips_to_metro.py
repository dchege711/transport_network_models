
# Created by Sam Bernstein on Nov. 26.
# 
# This program will take in Kornhauser's trip data after it is pruned
# to only include trips that could plausibly be taken along the Chicago
# metro, and use our model to sum up the expected number of people
# taking the Chicago metro from station A to station B for every
# ordered pair of nodes (A, B) in the metro system.

# This program will not calculate the flow through the network;
# that task will be left to another program.

import networkx as nx
import matplotlib.pyplot as plt
from metro_parts import *

import pickle




