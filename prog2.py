#!/usr/bin/python3

import pandas as pd;
import os;
import sys;
import codecs;


total = pd.Series()
myList = ['count']
path = os.walk("/root/data/")
for r,d,fi in path:
	for file in fi:
		if file.endswith(".csv"):
			fullpath = os.path.join(r,file);
			#Check if a file is empty
			if not os.stat(fullpath).st_size:
				continue;
			try:
				data = pd.read_csv(fullpath,low_memory=False,encoding='latin1');
			except:
				#Try if the csv file is using tabs as a delimiter
				try:
					data = pd.read_csv(fullpath,encoding='latin1',sep='\t');
				except:	
					#Check if the csv file contains only blank spaces or new lines
					with open(fullpath,'r') as thisfile:
						this = 	thisfile.read()
						if this.isspace():
							thisfile.close();
							continue
					thisfile.close();
			for (columnName,columnData) in data.iteritems():
				hist = columnData.value_counts();
				total = total.add(hist,fill_value=0);
total.to_csv('Output.csv',float_format='%g',index_label='value',header=myList,encoding='utf8')
