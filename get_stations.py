import csv

metro_file = open('CTA_L_Stops.csv', "r")


stations = set()

for line in metro_file:

     line = line.split(",")
     print(line[15])
     print(line[16])
     stations.add(line[3] + "," + line[16][1:] + ",")


print(stations)
print()
print()

for l in stations:
     print(l)



