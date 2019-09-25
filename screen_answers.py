import csv
import fnmatch
import os
import operator
from collections import OrderedDict

def main():

    field_count = 0
    file_count = 0
    row_count = 0
    fields = {}

    for root, dirnames, filenames in os.walk('data'):
        for filename in fnmatch.filter(filenames, '*.csv'):
            file_path = os.path.join(root, filename)
            with open(file_path) as file:
                file_count += 1
                reader = csv.reader(file)
                row_num = 0
                try:
                    for row in reader:
                        row_num += 1
                        if (row_num == 1):
                            num_fields = len(row)
                            field_count += num_fields
                        else:
                            row_count += 1
                            for value in row:
                                value = value.strip()
                                if not value in fields:
                                    fields[value] = 1
                                else:
                                    fields[value] = fields[value] + 1
                except:
                    print('Error processing file: %s' % file_path)

           
    print('what\'s the average number of fields across all the .csv files?: %s' % (field_count / file_count))

    write_csv(fields)

    print('Please see word_counts.csv in current directory for word counts.')

    print('what\'s the total number or rows for the all the .csv files?: %s' % row_count)

def write_csv(data):
    sorted_data = OrderedDict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    with open('word_counts.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['value', 'count'])
        for word in sorted_data:
            writer.writerow([word, sorted_data[word]])

if __name__== "__main__":
    main()