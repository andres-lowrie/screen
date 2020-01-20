
import csv
import os
from functools import reduce
from file_processing import CSV_Proc


def main():

    
    rootdir = '/root/data'
    #rootdir = '/Users/jmiracles80/data/ppp/data'
    fnames = []

    file_out = './count.csv'
    row_num = 0
    wrd_cnt = {}
    file_num = 0


    cp = CSV_Proc(wrd_cnt,row_num)

    try:
        #walk through every sub directory to get only the csv files
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if file.endswith('.csv'):
                    fnames.append(str(os.path.join(subdir,file)))
                    file_num +=1

    except Exception as e:
        print(e)

    wdCntDict = {}
    total = 0
    iter_csv = iter(cp.process_file(fnames))
    next(iter_csv)  # Skipping the column names
    #iterate through each row
    for row in iter_csv:
        total += 1
        #iterate through each column in rwo
        for x in row:
            if x in wdCntDict.keys():
                wdCntDict[x] += 1
            else:
                wdCntDict[x] = 1
    
    # write dict out to file
    cp.write_dict(wdCntDict,file_out)

    print("# Questions")

    print("## what's the average number of fields across all the `.csv` files?")
    print(cp.col_count(fnames))

    print("## create a csv file that shows the word count of every value of every dataset (dataset being a `.csv` file)")
    print(file_out)

    print("## what's the total number or rows for the all the `.csv` files?")
    print(total)

    

if __name__ == "__main__":

    main()

    