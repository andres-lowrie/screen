import csv
import logging
import os
import pathlib
from collections import Counter

DATA_DIR = './data'
OUTPUT_DIR = './output'
logger = logging.getLogger()
logger.setLevel(os.getenv('LOG_LEVEL', 'ERROR'))


def get_csv_data(file_name, encoding='utf-8'):
    data = None
    abs_path = os.path.abspath(f'{DATA_DIR}/{file_name}')
    with open(os.path.abspath(abs_path), encoding=encoding) as f:
        try:
            data = list(csv.reader(f))
        except Exception as ex:
            logger.debug(ex)
    return data


def write_word_count_csv(counter, file_name='word_count.csv'):
    pathlib.Path(os.path.abspath(OUTPUT_DIR)).mkdir(parents=True, exist_ok=True)
    with open(os.path.abspath(f'{OUTPUT_DIR}/{file_name}'), 'w') as word_count_file:
        writer = csv.writer(word_count_file, dialect='unix')
        writer.writerow(('word', 'count'))
        writer.writerows(counter.items())


def get_csv_files(csv_list_file):
    with open(os.path.abspath(f'{DATA_DIR}/{csv_list_file}')) as csv_files:
        csv_files = csv_files.readlines()
    return csv_files


def process():
    csv_list_file = 'csv_files.txt'
    field_count = 0
    row_count = 0
    word_counter = Counter()

    csv_files = get_csv_files(csv_list_file)

    for file_name in csv_files:
        file_name = file_name.strip()
        logger.info(f'csv file name: {file_name}')
        csv_data = get_csv_data(file_name)
        csv_data = csv_data if csv_data else get_csv_data(file_name, encoding='cp1252')
        size = len(csv_data)
        logger.info(f'all rows including header: {size}')
        row_count += size - 1
        field_count += len(csv_data[0])
        logger.info(f'number of columns: {field_count}')
        for i in range(1, size):
            word_counter.update(csv_data[i])

    return (field_count/len(csv_files)), row_count, word_counter


if __name__ == "__main__":
    average_fields, total_rows, word_count = process()
    # what's the average number of fields across all the .csv files?
    open(os.path.abspath(f'{OUTPUT_DIR}/average_fields'), 'w').write(str(average_fields))

    # create a csv file that shows the word count of every value of every dataset (dataset being a .csv file)
    write_word_count_csv(counter=word_count, file_name='word_count.csv')

    # what's the total number or rows for the all the .csv files?
    open(os.path.abspath(f'{OUTPUT_DIR}/total_rows'), 'w').write(str(total_rows))

