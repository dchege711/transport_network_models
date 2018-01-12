
import utilities as ut
import kd_methods
import random
import average_day_rates

testing = False

def add_origin_stations_to_pruned_data():

    origin_lat_index = 7
    origin_lng_index = 6

    tree = kd_methods.KdTree()

    input_file_name = 'pruned_kornhauser_chicago.csv' # 'sample_subset_pruned_kornhauser.csv' #
    output_file_name = 'pruned_kornhauser_w_origins.csv' # 'pruned_kornhauser_w_origins_test.csv' # 

    if testing:
        input_file_name = 'sample_subset_pruned_kornhauser.csv'
        output_file_name = 'pruned_kornhauser_w_origins_test.csv'

    input_file = open(input_file_name, 'r')
    output_file = open(output_file_name, 'w')

    header = input_file.readline() # Ignore the header
    output_file.write(header[:-1] + ",Origin Station\n")

    status_every = 500000

    print("Writing origins to: " + output_file_name)
    counter = 0
    for line in input_file:

        items = line.split(",")
        start_lat = float(items[origin_lat_index])
        start_lng = float(items[origin_lng_index])
        origin_station = tree.nearest(start_lat, start_lng)[0]

        output_file.write(line[:-1] + "," + ut.decomma(origin_station) + "\n")

        counter += 1
        if counter % status_every == 0:
            print("Processed", str(counter), "lines")

    input_file.close()
    output_file.close()
    print("\nDone\n")

def sort_by_origin_station():

    input_file_name = 'pruned_kornhauser_w_origins.csv' # 'pruned_kornhauser_w_origins_test.csv' #
    output_file_name = 'pruned_kornhauser_w_origins_sorted.csv' # 'pruned_kornhauser_w_origins_sorted_test.csv' #

    if testing:
        input_file_name = 'pruned_kornhauser_w_origins_test.csv'
        output_file_name = 'pruned_kornhauser_w_origins_sorted_test.csv'

    input_file = open(input_file_name, 'r')
    output_file = open(output_file_name, 'w')

    header = input_file.readline() # Copy the header
    output_file.write(header)

    all_trips = []

    origin_station_index = 19

    status_every = 500000

    print("Sorting trips in", input_file_name, "by origin.")
    print("Writing sorted results to: ", output_file_name)
    counter = 0
    # Read in all trips into a list of trips
    for line in input_file:

        items = line.split(",")
        all_trips.append(items)

        if counter % status_every == 0:
            print("So far added to all_trips", str(counter), "lines")
        counter += 1

    # sort the list of trips by origin station name
    print("All lines added to all_trips. Sorting now.")
    all_trips.sort(key = lambda trip: trip[origin_station_index])

    # Write the list of trips sorted by origin station to the output file
    counter = 0
    for trip in all_trips:
        output_file.write(",".join(trip))

        if counter % status_every == 0:
            print("So far wrote", str(counter), " sorted lines to output file.")
        counter += 1
    print("Wrote", str(counter), "lines to output file.")

    input_file.close()
    output_file.close()
    print("\nDone\n")


def sample_from_sorted_origins():

    input_file_name = 'pruned_kornhauser_w_origins_sorted.csv' # 'pruned_kornhauser_w_origins_sorted_test.csv' # 
    output_file_name = 'sampled_kornhauser_trips.csv' # 'sampled_kornhauser_trips_test.csv' # 

    if testing:
        input_file_name = 'pruned_kornhauser_w_origins_sorted_test.csv'
        output_file_name = 'sampled_kornhauser_trips_test.csv'

    # Initializes object that has getRidership(node) method that
    # returns the avg ridership at that node
    Avgs = average_day_rates.AvgRidership()

    input_file = open(input_file_name, 'r')
    output_file = open(output_file_name, 'w')

    header = input_file.readline() # Copy the header
    output_file.write(header)

    all_trips = []

    origin_station_index = 19

    status_every = 500000

    print("Sampling from: " + input_file_name)
    print("Writing sampled results to: " + output_file_name)

    # Go through each trip, adding it to the list of the current origin
    # station, and if a new origin station is reached, randomly sample
    # from the amassed last origin stations and write them to the 
    # output file.
    counter = 0
    sample_counter = 0

    # Handle first line to initialize stuff
    current_station_trips = []
    first_line = input_file.readline()
    items = first_line.split(",")
    current_origin_station = items[origin_station_index].strip()
    current_station_trips.append(first_line)

    for line in input_file:

        items = line.split(",")

        if items[origin_station_index].strip() != current_origin_station:

            # Set k to the avg number of people who get on at the current_origin_station
            k = int(Avgs.getRidership(current_origin_station))

            sampled_trips = []
            # print(current_origin_station, ":", k)
            if k > len(current_station_trips):
                if not testing: print("ATTENTION: STATION", current_origin_station, "HAD FEWER PRUNED KORNHAUSER DATA OCCURRENCES THAT IT'S AVERAGE RIDERSHIP VALUE")
                
                for i in range(k):
                    sampled_trips.append(random.choice(current_station_trips))

            else:
                sampled_trips = random.sample(current_station_trips, k)

            for f in sampled_trips:
                output_file.write(f)
            sample_counter += k

            current_origin_station = items[origin_station_index].strip()
            current_station_trips = []
        
        current_station_trips.append(line)

        if counter % status_every == 0:
            print("Went through", str(counter), "lines")
        counter += 1


    print("len of current_station_trips = ", len(current_station_trips))
    # print("current_station_trips = \n", current_station_trips)
    # Handle edge case of last origin station


    k = int(Avgs.getRidership(current_origin_station))
    sampled_trips = []
    # print(current_origin_station, ":", k)
    if k > len(current_station_trips):
        if not testing: print("ATTENTION: STATION", current_origin_station, "HAD FEWER PRUNED KORNHAUSER DATA OCCURRENCES THAT IT'S AVERAGE RIDERSHIP VALUE")
        
        for i in range(k):
            sampled_trips.append(random.choice(current_station_trips))
    else:
        sampled_trips = random.sample(current_station_trips, k)

    for line in sampled_trips:
        output_file.write(line)
    sample_counter += k

    print("Wrote", str(sample_counter), "sampled trips to the output file")

    input_file.close()
    output_file.close()
    print("Done")


if __name__ == "__main__":

    # print("\nADDING ORIGIN STATIONS TO PRUNED DATA\n\n")
    # add_origin_stations_to_pruned_data()
    # print("\n\nSORTING BY ORIGIN STATION \n\n")
    # sort_by_origin_station()
    print("\n\nSAMPLING FROM SORTED ORIGIN STATIONS \n\n")
    sample_from_sorted_origins()





