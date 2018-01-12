"""
average_day_rates.py

Given the amount of people getting into a station per day (as provided
by the Chicago Transport Authority) in 2010, we find the average number
of people getting into a station.

"""
import utilities as ut
import map_kornhauser_to_metro
import csv
import pickle
import csv

avg_data_before_correct_station_names = "average_ridership_data_before_correct_stations.csv"
avg_data_csv_name = "average_ridership_data.csv"
avg_data_pkl_name = "average_ridership_dict.pkl"

class AvgRidership:

    default_val = 'default'
    def __init__(self):

        # Read in the dict with avg ridership for each station from the pickle file
        pkl_file_path = ut.get_path(avg_data_pkl_name)
        input_file = open(pkl_file_path, 'rb')
        self.avg_ridership = pickle.load(input_file)
        input_file.close()

    def getRidership(self, station_name):
        try:
            val = self.avg_ridership[station_name]
            return val
        except:
            return self.avg_ridership[AvgRidership.default_val]


def write_pkl():
    Node_Dictionary = {}
    input_file = open(avg_data_csv_name, "r")

    input_file.readline() #ignore headers

    for line in input_file:
        items = line.split(",")
        node_name, avg = items[0], float(items[1])
        Node_Dictionary[node_name] = avg

    print("Printing Node_Dictionary:\n")

    for x in Node_Dictionary:
        print(x + ": " + str(Node_Dictionary[x]))

    pkl_file_path = ut.get_path(avg_data_pkl_name)
    output_file = open(pkl_file_path,'wb')
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
    # write_pkl()
    Avgs = AvgRidership()

    # stations = ['Fullerton (Red, Brown & Purple Lines)','51st (Green Line)','Berwyn (Red Line)','Jarvis (Red Line)']
    # for f in stations:
    #     print(f, "=", avgs.getRidership(f))

    with open('node_names.txt') as f:
        node_names = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    node_names = [x.strip() for x in node_names] 

    total = 0
    for node in node_names:
        rides = int(Avgs.getRidership(ut.decomma(node)))
        # print(node, "=", rides)
        total += rides


    print("Total = ", total)
    print()

    tot = 0
    for key in Avgs.avg_ridership:
        tot += int(Avgs.avg_ridership[key])


    print("Just dict values total = ", tot)






