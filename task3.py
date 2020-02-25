'''
Uses pandas to read each csv file based on matched path /root/data/{data source}/data/*.csv
Adds row count to total

Note:
Code ignores csv files in Archieves folder to avoid duplicate content as files in data folder are generated from archieved files
Prints a message containing file names if file is empty/failed processing
Handles land-matrix which contains ; seperated values
'''

import glob
import pandas as pd
import csv
import math
import sys
import os


total=0
path= '/root/data/**/data/*.csv'

# Validates the container has the directory containing Data sources
if not os.path.exists('/root/data/'):
       raise Exception('Data path is not available! Check build process!')

# Iterates through all the source files
for x in glob.glob(path, recursive=True):
    try:
           df = pd.read_csv(x, encoding = "ISO-8859-1",low_memory=False,quotechar='"',skipinitialspace=True)
           total+= len(df.index)
    except pd.io.common.EmptyDataError:
           print('Contents empty. Review file:'+x)
    except pd.errors.ParserError:
           try:
              df = pd.read_csv(x,sep=';',quotechar='"',skipinitialspace=True)
              total+= len(df.index)
           except:
              print('Unknown Exception. Review file:'+x)
    except:
              print('Unknown Exception. Review file:'+x)

print(total)
with open('output/Totalcount.csv', 'w') as f:
        f.write(str(total))