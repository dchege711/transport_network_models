import csv

metro_file = open('CTA_L_Stops.csv', "r")


stations = set()

for line in metro_file:

     line = line.split(",")
     stations.add(line[3])


print(stations)
print()
print()

for l in stations:
     print(l)



