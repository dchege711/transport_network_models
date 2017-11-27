"""
Kornhauser's data contains more data points than we can consider for the
metro. This file cuts down on the number that we have to consider.

"""

# Relevant Indexes. Get these from the .csv files
# Make sure that all csv files have the same format
origin_lat_index = 7
origin_lng_index = 6
dest_lat_index = 15
dest_lng_index = 14
trip_distance_index = 18

# Trimming parameters. Adjust these to filter the csvs
west_limit = -88.6 # O'Hare, 41.97766526, -87.90422307
north_limit = 42.8 # Linden, 42.073153, -87.69073
south_limit = 41 # 95th/Dan Ryan, 41.722377, -87.624342
trip_distance_limit = 25 # Maximum length of a trip by the metro

csv_file_names = ["FinalOriginPixel17031_1.csv"]

def prune_csv_data(csv_files):
    output_file = open('pruned_kornhauser_chicago.csv', 'w')
    counter = 0
    for csv_file_name in csv_file_names:
        with open(csv_file_name, 'r') as csv_file:
            header = csv_file.readline() # Ignore the header
            if counter == 0:
                output_file.write(header)

            # Prune the data. Fail fast
            for next_line in csv_file:
                items = next_line.split(",")

                if items[trip_distance_index] > trip_distance_limit:
                    continue

                if items[origin_lat_index] > north_limit or items[origin_lat_index] < south_limit:
                    continue

                if items[dest_lat_index] > north_limit or items[dest_lat_index] < south_limit:
                    continue

                if items[origin_lng_index] < west_limit or items[dest_lng_index] < west_limit:
                    continue

                output_file.write(next_line)

        counter += 1
