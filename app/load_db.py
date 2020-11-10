from glob import glob
from sqlalchemy import create_engine
import pandas as pd
import os

def get_all_csv_paths(data_path, csv_ext):

    data_csv_files = []

    for path, subdir, files in os.walk(data_path):
        for file in glob(os.path.join(path, csv_ext)):
            data_csv_files.append(file)

    return data_csv_files

def create_db_connection(db_name):

    engine = create_engine(db_name, echo=True)
    sqlite_connection = engine.connect()
    return sqlite_connection

def create_table_in_db(data_csv_files):
    for i in data_csv_files:
        base = os.path.basename(i)
        table_name = os.path.splitext(base)[0]
        try:
            table_pdf = pd.read_csv(i, error_bad_lines=False)
            table_pdf.to_sql(table_name, sqlite_connection, if_exists='fail')
        except Exception as e:
            #TODO FIX TABLES
            print(str(e), i)

if __name__ == "__main__":
    data_path = "/root/data"
    csv_ext = "*.csv"
    db_name = "sqlite:///super_random.db"

    data_csv_files = get_all_csv_paths(data_path, csv_ext)
    sqlite_connection = create_db_connection(db_name)
    create_table_in_db(data_csv_files)
    sqlite_connection.close()
