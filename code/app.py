
from flask import Flask, send_file
import os,time
import operator
import collections
from collections import Counter
from operator import itemgetter
import pandas as pd
import os.path
import sys
import csv
from collections import OrderedDict
import os
import itertools




app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello'


#what's the average number of fields across all the .csv filterles?
@app.route('/csv_quest1')
def csv_quest1():
    filenames = []
    num_cols=[]

    for subdir, dirs, files in os.walk(r'/root/data'):
        for file in files:
            if file.endswith(".csv"):
                filenames.append(os.path.join(subdir, file))

    print(filenames)


    for filename in filenames:
        try:
            print(filename)
            with open(filename,'r') as csvfile:
                csv_dict = [row for row in csv.DictReader(csvfile)]
                if len(csv_dict) == 0:
                    continue
                else:
                    df = pd.read_csv(filename, encoding='ISO-8859-1', error_bad_lines=False, skip_blank_lines = False)
                    print(df.head())
                    num_cols.append(len(df.columns))
        except UnicodeDecodeError:
            pass
    average_columns= sum(num_cols)/len(num_cols)
    return '%f' % average_columns


         
#what's the total number or rows for the all the .csv files?
@app.route('/csv_quest2')
def csv_quest2():
    filenames = []
    num_cols=[]
    
    for subdir, dirs, files in os.walk(r'/root/data'):
        for file in files:
            if file.endswith(".csv"):
                filenames.append(os.path.join(subdir, file))
    print("from second question")

    print(filenames)
    mainlist = []
    data = []
    dd=[]


    for filename in filenames:
        try:
            print(filename)
            with open(filename,'r') as csvfile:
                csv_dict = [row for row in csv.DictReader(csvfile)]
                if len(csv_dict) == 0:
                    continue
                else:
                    with open(filename, newline='') as f:
                        reader = csv.reader(f)
                        dd=list(reader)
                        data.extend(dd)
        except UnicodeDecodeError:
            pass

    for list1 in data:
        mainlist.extend(list1)

    counts = {}
    counts = Counter(mainlist)
    my_dict = dict(counts)
    with open('test.csv', 'w') as f:
        f.write("%s,%s\n"%("value","count"))
        for key in my_dict.keys():
            f.write("%s,%s\n"%(key,my_dict[key]))
    return send_file('test.csv', as_attachment=True)


    
 

    
    
#what's the total number or rows for the all the .csv files?
@app.route('/csv_quest3')
def csv_quest3():
    filenames = []
    num_rows=[]
    
    for subdir, dirs, files in os.walk(r'/root/data'):
        for file in files:
            if file.endswith(".csv"):
                filenames.append(os.path.join(subdir, file))


    print(filenames)

    for filename in filenames:
        try:
            print(filename)
            with open(filename,'r') as csvfile:
                csv_dict = [row for row in csv.DictReader(csvfile)]
                if len(csv_dict) == 0:
                    continue
                else:
                    df = pd.read_csv(filename, encoding='ISO-8859-1', error_bad_lines=False, skip_blank_lines = False)
                    num_rows.append(df.shape[0] + 1)
        except UnicodeDecodeError:
            pass
    total_rows= sum(num_rows)
    return ' %f' % total_rows







if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

