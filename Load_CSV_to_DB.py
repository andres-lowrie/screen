import os
import re
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql://root:1234@localhost/TEST?charset=utf8', echo=False)
file_path ="./data"

csv_name_reg = r'^.*csv$'

for root, _, files in os.walk(file_path):
    for thefile in files:
        match_name = re.match(csv_name_reg, str(thefile))
        if match_name:
            print(thefile)
            files_path = os.path.join(root,thefile)
            try:
                df = pd.read_csv(files_path, encoding='utf-8')
                df.to_sql(name=thefile.split(".")[0].replace('-', '_').replace(' ','_'), if_exists='replace', con=engine, index=False)
            except:
                print('The file name ' + thefile + ' has error')
