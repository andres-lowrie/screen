import os
import pandas
import numpy as np
import time
import math


# Get all CSV files
def get_csv_files():
    csv_file_list = []
    try:
        for root, dirs, files in os.walk("/root/data"):
            for file in files:
                if file.endswith(".csv"):
                    csv_file_list.append(os.path.join(root, file))
    except Exception as e:
        print("Exception occurred in get_csv_files()")
        print(e)
    return csv_file_list


# Read data from CSV using pandas
def open_with_pandas_read_csv(fileName):
    df = pandas.DataFrame()
    try:
        df = pandas.read_csv(fileName, error_bad_lines=False, skipinitialspace=True, quotechar='"',warn_bad_lines=False)
    except Exception as e:
        print("Exception occurred while reading: "+str(fileName))
        print(e)
    return df

def value_counter(value):
    if type(value) is str and 'nan' not in value:
        if value in value_count:
            value_count[value] = value_count[value]+1
        else:
            value_count[value] = 1


value_count = {}


def main():
    total_number_of_rows = 0
    total_number_of_columns = 0
    csv_files = get_csv_files()
    if len(csv_files) > 0:
        print("Total Number of csv files: "+str(len(csv_files)))
        for file in csv_files:
            df = open_with_pandas_read_csv(file)
            if not df.empty:
                total_number_of_rows = total_number_of_rows+len(df.values)
                total_number_of_columns = total_number_of_columns + len(list(df))
                temp = np.array(df.values).tolist()
                for data in temp:
                    [value_counter(value) for value in data]
            else:
                print("Empty file: "+str(file))

        print("ANSWER3: Total Number of Rows: "+str(total_number_of_rows))
        print("ANSWER1: Average number of fields: "+str(math.ceil(total_number_of_columns/len(csv_files))))
        out = pandas.DataFrame([(k, value_count[k]) for k in sorted(value_count, key=value_count.get, reverse=True)],
                               columns=['value', 'count'])
        try:
            out.to_csv("/root/output/value_count.csv")
            print("ANSWER2: Value count csv generated: /root/output/value_count.csv")
        except Exception as e:
            print("Exception occurred while creating ")
    else:
        print("No CSV files found")

if __name__ == '__main__':
    print("Started processing csv files")
    start_time = time.clock()
    main()
    print('Total time taken: ' + str(time.clock() - start_time), "seconds")
