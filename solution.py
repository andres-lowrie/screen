from pathlib import Path
from collections import defaultdict


files=[]
total_number_of_rows=0
total_number_of_fields=0
value_WordCount=defaultdict(int)

for x in Path('/root/data/').glob("**/*.csv"):
    files.append(str(x))


for y in files:
    with open(y,"rb") as f:
        for line_number,line in enumerate(f,1):
            if line_number==1:
                total_number_of_fields=total_number_of_fields+len(line.decode("cp437").split(","))
            else:
                row_values=str(line.decode("cp437")).split(",")
                for val in row_values:
                    val=val.rstrip()
                    value_WordCount[val]=value_WordCount[val]+1

        total_number_of_rows=total_number_of_rows+line_number

#print("total_number_of_fields:" + str(total_number_of_fields)+"\n")
#print("number of files: " + str(len(files)) + "\n")
#print("total number of rows: " + str(total_number_of_rows))

with open("/root/avg_number_of_fields.txt","w") as h:
    h.write(str(total_number_of_fields/len(files)))

with open("/root/total_number_of_rows.txt","w") as i:
    i.write(str(total_number_of_rows))


with open("/root/value_WordCount.csv","wb") as g:
    g.write(b"value,count")
    g.write(b"\n")
    for key in value_WordCount.keys():
        g.write(key.encode("cp437"))
        g.write(b",")
        g.write(str(value_WordCount[key]).encode("cp437"))
        g.write(b"\n")
