#!/usr/bin/python3

import pandas as pd;
import os;

total = 0;
count = 0;
path = os.walk("/root/data/")
for r,d,fi in path:
	for file in fi:
		if file.endswith(".csv"):
			count = count+1;
			fullpath = os.path.join(r,file);
			#print("\n" + fullpath);
			if not os.stat(fullpath).st_size:
				continue;
			try:
				data = pd.read_csv(fullpath,low_memory=False,encoding='latin1');
			except:
				try:
					data = pd.read_csv(fullpath,encoding='latin1',sep='\t');
				except:	
					with open(fullpath,'r') as thisfile:
						this = 	thisfile.read()
						if this.isspace():
							thisfile.close();
							continue
					thisfile.close();
			#print("Number of columns in "+ fullpath + ": ")
			total += len(data.columns);
			#print(len(data.columns));
#print("\n\nTotal: ");
#print(total);
#print("\n\nAvg: ");
print(round(total/count));
