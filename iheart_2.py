#############################
#Manuel I. De Aguinaga
#############################

import pandas as pd
import csv

def main():
        avg_num = 0
        directors = open("DOTcsvFiles.txt", "r")
        files = directors.read().splitlines()


        with open('TotalCount.csv', 'w', newline='') as file:
                wf = csv.writer(file)
                wf.writerow(["Value", "Count"])

                for f in files:
                        try:
                                df = pd.read_csv(f, low_memory=False)
                                wf.writerow([f,df.shape[0]*df.shape[1] ])

                        except:
                                error = "FILE has a wrong format or is not a CSV file"
        print("file TotalCount.csv as being created")
        directors.close()

if __name__ == '__main__':
        main()
