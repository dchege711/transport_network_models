"""
Provide an interface for using the k-d tree.

Suggestion: Can bundle this with the graph?

The current format requires us to create the graph AND the KdTree. I suggest
that when we're creating the graph, I also implement a k-d tree under the
hood.
Clients of the transport network can then call nearest() on the graph itself,
without caring whether we have a k-d tree under the hood or not.

"""
import metro_parts
import kdtree
import utilities as ut

class KdTree():

    # creates the k-d tree from the nodes lat/long file
    def __init__(self):

        # Create an empty tree of 2 dimensions for lat,long
        self.tree = kdtree.create(dimensions=2)
        stations_file = open(ut.get_path("nodes_with_latlng_updated.txt"), "r")

        # Read each station into the kdtree
        for line in stations_file:

            station_details = line.strip().split("\t")
            lat_lng = station_details[1].split(",")
            lat = float(lat_lng[0])
            lng = float(lat_lng[1])
            coords = (lat, lng)
            name = station_details[0]
            self.tree.add(metro_parts.Station(name, coords))    # Station is a class in metro_parts

        self.tree = self.tree.rebalance()
        print("Created the", self.tree.dimensions, "-d tree")

    # returns tuple of (station name, coords, dist) for the nearest station
    def nearest(self, lat, lon):

        tup = self.tree.search_nn((lat, lon))
        name = tup[0].data.name
        dist = tup[1]

        return (name, dist)

def test_methods():
    t = KdTree()

    test = (1,2)
    res = t.nearest(test[0], test[1])
    print("Nearest node to " + str(test) + " is:")
    print(res)
    print()

    # Find the nearest node to the location (1, 2, 3)
    # print(tree.search_nn(test[0], test[1] )[0].data.name)

if __name__ == "__main__":
    test_methods()
