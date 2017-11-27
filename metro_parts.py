

# file name of the pickle file that contains the created metro graph
graph_pickle_file_name = "metro_graph.pkl"

station_kdtree_file_name = "station_kdtree.pkl"

class MetroNode():

    def __init__(self, name):

        self.name = name

    def __str__(self):

        return self.name

    def __hash__(self):

        return hash(str(self.name))

    # if statements allow MetroNodes to be compared to
    # strings as well as other MetroNode objects
    def __eq__(self, other):

        if isinstance(other, str):
            return self.name == other

        elif isinstance(other, type(self)):
            return self.name == other.name

        return False

class MetroEdge():

    def __init__(self, daily_flow = None, weekly_flow = None):

        self.daily_flow = daily_flow
        self.weekly_flow = weekly_flow

    def setDaily(self, val):
        self.daily_flow = val

    def setWeekly(self, val):
        self.weekly_flow = val
