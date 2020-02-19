#############################
#Manuel I. De Aguinaga
#############################

import pandas as pd


def main():
        avg_num = 0
        directors = open("DOTcsvFiles.txt", "r")
        files = directors.read().splitlines()

        for f in files:
                try:
                        df = pd.read_csv(f,low_memory=False)
                        avg_num = avg_num + len(df.columns)

                except:
                        error = "FILE has a wrong format or is not a CSV file"
                avg = avg_num/len(files)
        print("AVERAGE: %0.0f"%(avg))
        directors.close()

if __name__ == '__main__':
        main()
