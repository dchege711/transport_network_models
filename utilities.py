"""
Handles operations that help keep our files organized.

"""
import os

# Maintain a directory of the files and the folders they're in
file_locations = {
    # Files for building the graph
    "nodes_with_latlng.txt" : "chicago_nodes_and_links",

    # Files containing edges for the graph
    "blue.txt"      : "chicago_nodes_and_links",
    "brown.txt"     : "chicago_nodes_and_links",
    "green.txt"     : "chicago_nodes_and_links",
    "orange.txt"    : "chicago_nodes_and_links",
    "pink.txt"      : "chicago_nodes_and_links",
    "purple.txt"    : "chicago_nodes_and_links",
    "red.txt"       : "chicago_nodes_and_links",
    "yellow.txt"    : "chicago_nodes_and_links",

    # Pickle files containing python data objects
    "metro_graph.pkl" : "pickle_files",
    "station_kdtree.pkl" : "pickle_files"
}

# This gets the directory of where utilities.py is located
# utilties.py should be kept at the root of the project
base_directory = os.path.dirname(os.path.abspath(__file__))

def get_path(file_name):
    # Locate the folder in which the file is in
    try:
        folder_name = file_locations[file_name]
    except KeyError:
        err = " ".join([
            "Could not find",
            file_name,
            "Check your spelling, or update my dict"
        ])
        raise KeyError(err)

    path_to_subfolder = os.path.join(base_directory, folder_name)
    return os.path.join(path_to_subfolder, file_name)
