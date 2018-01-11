"""
average_day_rates.py

Given the amount of people getting into a station per day (as provided
by the Chicago Transport Authority) in 2010, we find the average number
of people getting into a station.

"""

import csv
import pickle
import csv

avg_data_before_correct_station_names = "average_ridership_data_before_correct_stations.csv"
avg_data_csv_name = "average_ridership_data.csv"
avg_data_pkl_name = "average_ridership_dict.pkl"

class AvgRidership:

    def __init__(self):

        # Read in the dict with avg ridership for each station from the pickle file
        input_file = open(avg_data_pkl_name, 'rb')
        self.avg_ridership = pickle.load(input_file)
        input_file.close()

    def getRidership(self, station_name):

        return self.avg_ridership[station_name]

def write_pkl():
    Node_Dictionary = {}
    input_file = open(avg_data_csv_name, "r")

    input_file.readline() #ignore headers

    for line in input_file:
        items = line.split(",")
        node_name, avg = map_kornhauser_to_metro.recomma(items[0]), float(items[1])
        Node_Dictionary[node_name] = avg

    print("Printing Node_Dictionary:\n")

    for x in Node_Dictionary:
        print(x + ": " + str(Node_Dictionary[x]))

    output_file = open(avg_data_pkl_name,'wb')
    pickle.dump(Node_Dictionary, output_file)
    output_file.close()


def average_each_station():

    metro_file = open("CTA_Ridership.csv", "r")

    Node_Dictionary = {}
    Tot = 0
    Count = 0

    reader = csv.reader(metro_file)
    row1 = next(reader)
    check_name = (row1[1])
    check_value = (int)(row1[4])
    Tot += check_value
    Count += 1

    for line in metro_file:
         line = line.split(",")
         station_name = (line[1])
         rider_value = (int)(line[4])
         if(station_name == check_name):
             Tot += rider_value
             Count += 1
         else:
             Node_Dictionary[check_name] = Tot/Count
             Tot = 0
             Count = 0
             check_name = station_name
             Tot += rider_value
             Count += 1

    avgs_file = open(avg_data_before_correct_station_names, "w")
    avgs_file.write("Station Name,Avg Daily Ridership\n")
    for x in Node_Dictionary:
        # print(x + ": " + str(Node_Dictionary[x]))
        avgs_file.write(x + "," + str(Node_Dictionary[x]) + "\n")

    print()
    key_min = min(Node_Dictionary, key = Node_Dictionary.get)
    key_max = max(Node_Dictionary, key = Node_Dictionary.get)

    print("min: " + key_min, "=", Node_Dictionary[key_min])
    print("max: " + key_max, "=", Node_Dictionary[key_max])

    #print(Node_Dictionary)



if __name__ == "__main__":

    ###

    # Get node names from nodes_latlng file
    # in_file = open("nodes_with_latlng_updated.txt", "r")
    # output = open("node_names.txt", "w")

    # for line in in_file:

    #     station_details = line.strip().split("\t")
    #     output.write(station_details[0] + "\n")

    # output.close()


    ###

    # average_each_station()

    # ridership = AvgRidership()

    write_pkl()

    stations = ['Fullerton (Red, Brown & Purple Lines)','51st (Green Line)','Berwyn (Red Line)','Jarvis (Red Line)','']




