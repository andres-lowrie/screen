import pandas as pd
from sqlalchemy import create_engine
import sqlite3

def run_query(query, database):

    conn = sqlite3.connect(database)
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df

def create_db_connection(db_name):

    engine = create_engine(db_name, echo=True)
    sqlite_connection = engine.connect()
    return sqlite_connection


if __name__ == "__main__":
    read_db_name = "/root/super_random.db"
    write_db_name = "sqlite:////root/super_random.db"
    get_table_names_query = "SELECT name FROM sqlite_master WHERE type='table'"
    col_sum = 0
    row_sum = 0

    tables_df = run_query(get_table_names_query, read_db_name)
    total_tables = len(tables_df['name'])

    sqlite_connection = create_db_connection(write_db_name)

    for table_name in tables_df['name']:
        get_table_row_count_query = f"SELECT count(*) as c FROM '{table_name}'"
        get_cols = f"PRAGMA table_info('{table_name}')"

        #get length of cols for all tables
        cols_df = run_query(get_cols, read_db_name)
        col_sum += len(cols_df['name'])
        #get sum up all rows found
        row_sum += run_query(get_table_row_count_query, read_db_name)["c"].iloc[0]

    #create table in db
    average = [["1", col_sum/total_tables]]
    average_df = pd.DataFrame(average, columns =['Questiom', 'Answer'])
    average_df.to_sql("question1", sqlite_connection, if_exists='fail')

    total_row_sum = [["3", row_sum]]
    row_sum_df = pd.DataFrame(total_row_sum, columns =['Questiom', 'Answer'])
    row_sum_df.to_sql("question3", sqlite_connection, if_exists='fail')
    sqlite_connection.close()

    # conn = sqlite3.connect(read_db_name)
    # c = conn.cursor()
    # c.execute("SELECT * FROM question1")
    # print(c.fetchone())
    # c.execute("SELECT * FROM question3")
    # print(c.fetchone())
    # conn.close()
