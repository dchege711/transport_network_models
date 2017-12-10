

import csv
import utilities as ut


# These files were manually compiled. They have station names on a given line
lines_files = [
    'blue.txt', 'brown.txt', 'green.txt', 'orange.txt', 'yellow.txt', "pink.txt", "purple.txt", "red.txt"
]

for metro_line in lines_files:
    f = open(ut.get_path(metro_line), "r")

    in_paren = False
    output_file = open("./" + metro_line[:-4] + "_treated.txt", "w")
    while True:
        c = f.read(1)

        if not c:
            print("End of file")
            break
        if c == "(":
            in_paren = True
            output_file.write(c)
        elif c == ")":
            in_paren = False
            output_file.write(c)

        elif c == "," and not in_paren:
            output_file.write("\n")
        else:
            output_file.write(c)






        #print("Read a character:", c)


