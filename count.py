# To get the all csv files from the mentioned path and its sub directories
import os, re, csv, itertools
import math, sys
import pandas as pd

#First identify the csv files in mentioned path. This result will be used in subsequent scripts.
#Note:Path needs to be changed.
with open('C:\\Users\\Buvaneswaran\\Downloads\\data\\result.txt', 'w') as a:
    for path , subdirs, files in os.walk('C:\\Users\\Buvaneswaran\\data\\'):
        for filenames in files:
            if re.match("^.*.csv$", filenames):
                f = os.path.join(path,filenames)
                fn = f.rstrip('\r\n')
                a.write(str(fn))
                a.write('\n')
a.close()

paths = []


with open("C:\\Users\\Buvaneswaran\\Downloads\\data\\result.txt")as file:
    filecount = 0
    for line in file:
        line = line.rstrip()
        paths.append(line)
        filecount = filecount + 1
    print("Total files count is ", filecount)

    # The below part is to identify the column count. The result will be stored in columns.txt
    with open('C:\\Users\\Buvaneswaran\\Downloads\\data\\columns.txt', 'w') as cf:
        sumcolum = 0
        for singlefile in paths:
            #print(singlefile)
            exampleFile = open(singlefile, 'r', encoding="utf8", errors='ignore')
            reader      = csv.reader(exampleFile)
            ncol        = len(next(reader))  # Read first line and count columns
            sumcolum    = sumcolum + ncol
            #print('File name is:', singlefile, ncol)
            cf.write(str(ncol))
            cf.write('\n')
            exampleFile.seek(0)
    print("Total column counts in all files:",sumcolum)
    print("Average no. of columns in all files: (rounded to next integer value)", math.ceil(sumcolum/filecount))
    cf.close()

    # The below part is to identify the word count. The result will be stored in words.txt
    with open('C:\\Users\\Buvaneswaran\\Downloads\\data\\words.txt', 'w') as wf:
        for singlefile in paths:
            try:
                exampleFile = open(singlefile, 'r', encoding="utf8", errors='ignore')
                df = pd.read_csv(exampleFile,skip_blank_lines=True)
                words_count = df.count().sum()
                print(singlefile, words_count)
                wf.write(str(singlefile))
                wf.write(',')
                wf.write(str(words_count))
                wf.write('\n')
            except (pd.errors.EmptyDataError,pd.errors.ParserError ) as e:
                continue

    wf.close()

    # The below part is to identify the total row count. The result will be stored in Total.txt
    with open('C:\\Users\\Buvaneswaran\\Downloads\\data\\Total.txt', 'w') as tf:
        totalrowcount = 0
        for singlefile in paths:
            exampleFile = open(singlefile, 'r', encoding="utf8", errors='ignore')
            reader = csv.reader(exampleFile)
            row_count = sum(1 for row in reader)
            totalrowcount = totalrowcount + row_count
            #print(row_count)
        #print("file count is",filecount)
        tf.write(str(totalrowcount - filecount))
        print("Total row count in all files are ", (totalrowcount - filecount)) # file count subtraction is to remove the headers

    tf.close()
