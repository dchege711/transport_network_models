"""
Handles operations that help keep our files organized.
utilties.py should be kept at the root of the project

"""
import os
import shutil

# Maintain a directory of the files and the folders they're in
file_locations = {
    # Files for building the graph
    "nodes_with_latlng.txt" : "chicago_nodes_and_links",
    "nodes_with_latlng_updated.txt" : "chicago_nodes_and_links",

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
    "station_kdtree.pkl" : "pickle_files",

    # Files to help simulate flow on the network
    "cta_ridership_daily_totals.csv" : "cta_ridership_data"
}

# This gets the directory of where utilities.py is located
base_directory = os.path.dirname(os.path.abspath(__file__))

def get_path(file_name):
    """
    Return the path of the specified file.
    If the file name doesn't exist in the dictionary, raise a KeyError.

    """
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

def new_path(subfolder_name, file_name):
    """
    Create a new file inside the specified subfolder.
    Return the path to this file.

    If the subfolder did not exist, create a new subfolder, and include
    the file in the subfolder.

    """
    path_to_subfolder = os.path.join(base_directory, subfolder_name)
    if not os.path.isdir(path_to_subfolder):
        os.makedirs(os.path.join(path_to_subfolder))
    return os.path.join(path_to_subfolder, file_name)

def test_get_path():
    # Test get_path()
    print("Testing get_path() on existing keys...")
    test_filename = list(file_locations.keys())[0]
    if os.path.exists(get_path(test_filename)):
        print("PASSED!\n")
    else:
        print("FAILED! Is", test_filename, "in the", file_locations[test_filename], "subfolder?\n")

    print("Testing get_path() on non-existent keys...")
    test_filename = "some_random_non-existent_file.txt"
    try:
        get_path(test_filename)
        print("FAILED. Expected a KeyError\n")
    except KeyError:
        print("PASSED!\n")

def test_new_path():
    print("Testing new_path() on new file in new subfolder")
    my_new_path = new_path("testing", "some_random_non-existent_file.txt")
    try:
        with open(my_new_path, 'w') as new_file:
            new_file.write("How do you make holy water?")
            new_file.write("You boil the hell out of it.")
        print("PASSED!\n")
        shutil.rmtree(os.path.join(base_directory, "testing"))
    except Exception as e:
        print("FAILED!", e, end="\n\n")

def unit_tests():
    test_get_path()
    test_new_path()

if __name__ == "__main__":
    unit_tests()
