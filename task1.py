'''
Uses pandas to read each csv file based on matched path /root/data/{data source}/data/*.csv
Adds the count of columns in current dataframe to total value and maintains count of files

Note:
Code ignores csv files in Archieves folder to avoid duplicate content as files in data folder are generated from archieved files
Prints a message containing file names if file is empty/failed processing
Considers failed/empty files towards average count
Handles land-matrix which contains ; seperated values
Efficient as it loads only 1 row for each file
'''


import glob
import pandas as pd
import csv
import math
import sys
import os


path= '/root/data/**/data/*.csv'
total=0
n=0

# Validates the container has the directory containing Data sources
if not os.path.exists('/root/data/'):
       raise Exception('Data path is not available! Check build process!')

# Iterates through all the source files
for x in glob.glob(path, recursive=True):
    try:
           df = pd.read_csv(x, encoding = "ISO-8859-1", quotechar='"',skipinitialspace=True,nrows=1)
           total+= len(df.columns)
           n+=1
    except pd.io.common.EmptyDataError:
           print('Contents empty. Review file:'+x)
           n+=1
    except pd.errors.ParserError:
            try:
              df = pd.read_csv(x,sep=';',quotechar='"',skipinitialspace=True)
              total+= len(df.columns)
              n+=1
            except:
              print('Unknown Exception. Review file:'+x)
    except:
              n+=1
              print('Unknown Exception. Review file:'+x)

# Check for division by 0. Uses Floor to get Int value.
res =  0 if n==0 else math.floor(total/n)

print(res)
with open('output/avgfields.csv', 'w') as f:
        f.write(str(res))