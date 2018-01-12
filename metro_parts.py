"""
metro_parts.py

Question: Why do we have MetroNode and Station as different classes?
Encapsulates classes for objects that the find relevant. Currently has:
    MetroNode   : The nodes in our transport graph
    MetroEdge   : The edges in our transport network
    Station     : Details about a specific station (node) in the network
"""
import utilities as ut
from math import asin, sin, cos, sqrt, pi

graph_pickle_file_name = ut.get_path("metro_graph.pkl")
station_kdtree_file_name = ut.get_path("station_kdtree.pkl")

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

class Station():
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords # tuple (lat, long)
        self.lat = float(coords[0])
        self.lng = float(coords[1])
        self.lat_in_radians = self.lat * pi / 180
        self.lng_in_radians = self.lng * pi / 180

    def __getitem__(self, key):
        return self.coords[key]

    def __len__(self):
        return len(self.coords)

    def __str__(self):
        return self.name + " : " + str(self.coords)
      
    def __repr__(self):
        return " ".join([
            "Name:", self.name, "lat: ", str(self.lat),
            "lng: ", str(self.lng)
        ])
        
    def distance_to(self, other, units="km"):
        # https://en.wikipedia.org/wiki/Haversine_formula
        
        if units == "km":
            radius = 6363.97
        elif units == "miles":
            radius = 3954.387626
        else:
            raise ValueError("{0} units are not supported".format(units))
        
        hav_lat = (1 - cos(other.lat_in_radians - self.lat_in_radians)) / 2.0
        hav_lng = (1 - cos(other.lng_in_radians - self.lng_in_radians)) / 2.0
        cos_lats = cos(self.lat_in_radians) * cos(other.lat_in_radians)
        
        return 2 * radius * asin(sqrt(hav_lat + cos_lats * hav_lng))
        
        
def station_main():
    station_a = Station("A", [41.953508, -87.746416])
    station_b = Station("B", [41.947983, -87.744942])
    assert ("{0:.4f}".format(station_a.distance_to(station_b)) == "0.6256")
    assert (station_a.distance_to(station_b) == station_b.distance_to(station_a))
    
    
if __name__ == "__main__":
    station_main()
