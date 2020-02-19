#!/usr/bin/python3

#############################
# By Manuel I. DE Aguinaga
#############################

import pandas as pd

def main():
        total_rows = 0
        directors = open("DOTcsvFiles.txt", "r")
        files = directors.read().splitlines()

        for f in files:
                try:
                        df = pd.read_csv(f, low_memory=False)
                        total_rows = total_rows + df.shape[0]

                except:
                        error= "FILE has a wrong format or is not a CSV file"

        print("TOTAL ROWS:",total_rows)
        directors.close()

if __name__ == '__main__':
        main()
