
import pickle
import metro_parts

class KdTree():

    def __init__(self):
        # Read in the metro graph G from the pickle file
        input_file = open(metro_parts.station_kdtree_file_name,'rb')
        self.tree = pickle.load(input_file)
        input_file.close()

    # returns tuple of (station name, coords, dist) for the nearest station
    def nearest(self, lat, lon):

        tup = self.tree.search_nn((lat, lon))
        name = tup[0].data.name
        dist = tup[1]

        return (name, dist)


t = KdTree()

test_node = (1,2)
res = t.nearest(test_node)

print(res)
print()
print("Nearest node to " + str(test_node) + " is:")
# Find the nearest node to the location (1, 2, 3)
print(tree.search_nn( test_node )[0].data.name)
