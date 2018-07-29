import csv
import logging
import chardet
import glob
import os
import pathlib
from collections import Counter

DATA_DIR = './data'
OUTPUT_DIR = './output'
logger = logging.getLogger()
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))


def read_csv_file(filename):
    reader = None
    with open(filename, 'rb') as file:
        try:
            rawdata = file.read()
            result = chardet.detect(rawdata)
            logger.info(f'encoding: {result["encoding"]}, confidence: {result["confidence"]}, language {result["language"]}')
            data = rawdata.decode(encoding=result['encoding'])
            reader = csv.reader(data.splitlines(), dialect='unix')
        except Exception as ex:
            logger.error(f'filename: {filename} - error: {ex}')

    return reader


def write_word_count_csv(counter, filename='word_count.csv'):
    pathlib.Path(os.path.abspath(OUTPUT_DIR)).mkdir(parents=True, exist_ok=True)
    with open(os.path.abspath(f'{OUTPUT_DIR}/{filename}'), 'w') as word_count_file:
        writer = csv.writer(word_count_file, dialect='unix', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('word', 'count'))
        writer.writerows(counter.items())


def process():
    field_count = 0
    row_count = 0
    word_counter = Counter()
    file_count = 0
    for filename in glob.glob('**/*.csv', recursive=True):
        logger.info(f'file name: {filename}')
        reader = read_csv_file(filename)
        header = next(reader)
        field_count += len(header)
        for row in reader:
            word_counter.update(row)
            row_count += 1
        file_count += 1

    return (field_count/file_count), row_count, word_counter


if __name__ == "__main__":
    average_fields, total_rows, word_count = process()
    os.makedirs(os.path.dirname(f'{OUTPUT_DIR}/'), exist_ok=True)
    # what's the average number of fields across all the .csv files?
    open(os.path.abspath(f'{OUTPUT_DIR}/average_fields'), 'w').write(str(average_fields))

    # create a csv file that shows the word count of every value of every dataset (dataset being a .csv file)
    write_word_count_csv(counter=word_count, filename='word_count.csv')

    # what's the total number or rows for the all the .csv files?
    open(os.path.abspath(f'{OUTPUT_DIR}/total_rows'), 'w').write(str(total_rows))

