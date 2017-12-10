"""
Provide an interface for using the k-d tree.

Suggestion: Can bundle this with the graph?

The current format requires us to create the graph AND the KdTree. I suggest
that when we're creating the graph, I also implement a k-d tree under the
hood.
Clients of the transport network can then call nearest() on the graph itself,
without caring whether we have a k-d tree under the hood or not.

"""
import pickle
import metro_parts

class KdTree():

    def __init__(self):
        # Read in the metro graph G from the pickle file
        print(metro_parts.station_kdtree_file_name)
        input_file = open(metro_parts.station_kdtree_file_name,'rb')
        self.tree = pickle.load(input_file)
        input_file.close()

    # returns tuple of (station name, coords, dist) for the nearest station
    def nearest(self, lat, lon):

        tup = self.tree.search_nn((lat, lon))
        name = tup[0].data.name
        dist = tup[1]

        return (name, dist)

def test_methods():
    t = KdTree()

    test_node = (1,2)
    res = t.nearest(test_node)

    print(res)
    print()
    print("Nearest node to " + str(test_node) + " is:")
    # Find the nearest node to the location (1, 2, 3)
    print(tree.search_nn( test_node )[0].data.name)

if __name__ == "__main__":
    test_methods()
