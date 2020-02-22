'''
Uses pandas to read each csv file based on matched path /root/data/{data source}/data/*.csv
Flattens the Dataframe to extract each value of each row/column
Updaes a common dictionary in <Value,Frequency> format which is then dumped to output file.

Note: 
Code ignores csv files in Archieves folder to avoid duplicate content as files in data folder are generated from archieved files.
Values in output file are lower cased and no processing is done for punctuation / character sets 
Handles land-matrix which contains ; seperated values
'''

import glob
import pandas as pd
import csv
import math
import sys
import os
from collections import defaultdict
import codecs

result = defaultdict(int)
path= '/root/data/**/data/*.csv'

# Validates the container has the directory containing Data sources
if not os.path.exists('/root/data/'):
       raise Exception('Data path is not available! Check build process!')

# Flattens a Dataframe to extract all values and updates frequency in results dictionary
def updatecounts(df,path):
    try:
        df = df.astype(str)
        cols= df.columns
        l = df[cols].apply(lambda x : x.str.split()).values.ravel().tolist()
        for i in l:
            for j in i:
                result[str(j).lower()]+=1
    except Exception as e:
        print("Failed to update count for file:"+path)
        print(str(e))

# Iterates through all the source files
for x in glob.glob(path, recursive=True):
    try:
           df = pd.read_csv(x, encoding = "ISO-8859-1",low_memory=False,quotechar='"',skipinitialspace=True)
           updatecounts(df,x)
    except pd.io.common.EmptyDataError:
           print('Contents empty. Review file:'+x)
    except pd.errors.ParserError:
           try:
              df = pd.read_csv(x,sep=';',quotechar='"',skipinitialspace=True)
              updatecounts(df,x)
           except:
              print('Unknown Exception. Review file:'+x)

# Write output to disk
with codecs.open('output/wordcount.csv', 'w','utf-8') as f:
    f.write("value,count\n")
    for key in result.keys():
        f.write("%s,%s\n"%(key,result[key]))

