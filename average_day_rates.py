"""
average_day_rates.py

Given the amount of people getting into a station per day (as provided
by the Chicago Transport Authority) in 2010, we find the average number
of people getting into a station.

"""

import csv
import pickle
import utilities as ut

metro_file = open(ut.get_path('CTA_Ridership.csv'), "r")

# stations = set()
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

output_file = open("average_ridership_data.pkl",'wb')
pickle.dump(Node_Dictionary, output_file)
output_file.close()
# print(Node_Dictionary)
