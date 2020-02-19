#!/usr/bin/python3

import pandas as pd;
import os;
import sys;
import codecs;


t = 0;
count = 0;
path = os.walk("/root/data/")
for r,d,fi in path:
	for file in fi:
		if file.endswith(".csv"):
			fullpath = os.path.join(r,file);
			#if the file is null
                        if not os.stat(fullpath).st_size:
				continue;
			try:
				data = pd.read_csv(fullpath,low_memory=False,encoding='latin1');
			except:
				try:
					data = pd.read_csv(fullpath,encoding='latin1',sep='\t');
				except:	
                                        #if the file contains blank spaces only
					with open(fullpath,'r') as thisfile:
						this = 	thisfile.read()
						if this.isspace():
							thisfile.close();
							continue
					thisfile.close();
			count += len(data.index)
print(count)
