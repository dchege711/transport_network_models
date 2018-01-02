import pickle
import csv

avg_data_file_name = "average_ridership_data.pkl"

class AvgRidership:

    def __init__(self):

        # Read in the dict with avg ridership for each station from the pickle file
        input_file = open(avg_data_file_name, 'rb')
        self.avg_ridership = pickle.load(input_file)
        input_file.close()

    def getRidership(self, station_name):

        return self.avg_ridership[station_name]

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

    for x in Node_Dictionary:
        print(x + ": " + str(Node_Dictionary[x]))

    print()
    key_min = min(Node_Dictionary, key = Node_Dictionary.get)
    key_max = max(Node_Dictionary, key = Node_Dictionary.get)

    print("min: " + key_min, "=", Node_Dictionary[key_min])
    print("max: " + key_max, "=", Node_Dictionary[key_max])

    output_file = open(avg_data_file_name,'wb')
    pickle.dump(Node_Dictionary, output_file)
    output_file.close()
    #print(Node_Dictionary)



if __name__ == "__main__":

    # average_each_station()

    ridership = AvgRidership()

    stations = ['Fullerton (Red, Brown & Purple Lines)','51st (Green Line)','Berwyn (Red Line)','Jarvis (Red Line)','']




