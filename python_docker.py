import csv
import os
import re
import string
import collections
import itertools


class PythonDocker:
    # method of calculate average number of columns in all csv files
    def avg_valuecount_totalrows(self, path):
        numfiles = 0
        sum = 0
        count = 0
        data_dict = {}
        # recursively search for csv files inside subdirectories
        for root, dirs, files in os.walk(path, topdown=False):
            for f in files:
                if f.endswith('.csv'):
                    filepath = root + os.sep + f
                    with open(filepath, "r", encoding='latin-1') as my_file:
                        reader = csv.reader(my_file, delimiter=",")
                        # count total number of lines
                        data = list(reader)
                        count = count + len(data)
                        # get number of columns in a file
                        sum = sum + len(data[0])
                        numfiles = numfiles + 1

                        # create data dictionary of words and counts to be written to csv file
                        counter = collections.Counter(itertools.chain(*data))
                        if (len(data_dict) == 0):
                            data_dict = dict(counter)
                        else:
                            for item in counter.keys():
                                if item in data_dict:
                                    data_dict[item] = data_dict.get(item) + counter.get(item)
                                else:
                                    data_dict[item] = 1
        if numfiles > 0:
            print("---------------------------------")
            print(round(sum / numfiles))
            print("---------------------------------")
        else:
            print("---------------------------------")
            print(sum)
            print("---------------------------------")

        print("Writing value-count pairs to words.csv file..")
        # write to the csv file in the format of key value pairs
        output_file = open("./words.csv", "w", newline='', encoding='latin-1')
        writer = csv.writer(output_file)
        writer.writerow(['value', 'count'])
        for word in data_dict.keys():
            writer.writerow([word, data_dict.get(word)])
        print("Done writing to words.csv")
        print("---------------------------------")

        print("Total number of rows:")
        print("---------------------------------")
        print(count)
        print("---------------------------------")


obj = PythonDocker()
path = "."
print("---------------------------------")
print("Average number of columns:")
obj.avg_valuecount_totalrows(path)