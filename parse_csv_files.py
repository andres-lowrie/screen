import chardet
import csv
import pathlib


def get_csv_list():
    return sorted(pathlib.Path('data').glob('**/*.csv'))

def get_encoding(filename):
    with open(filename, "rb") as rawdata:
        result = chardet.detect(rawdata.read())
    return result['encoding']

def parse_csv_files(csv_list):
    results = {}
    total_num_of_rows = 0
    field_count = []
    words = {}

    print("There are {} csv files to parse".format(len(csv_list)))
    for index, filename in enumerate(csv_list):
        encoding = get_encoding(filename)
        print("{}: Parsing {} with encoding {}".format(index, filename, encoding))
        with open(filename, 'r', encoding=encoding) as f:
            rows = csv.reader(f)
            for row_number, row in enumerate(rows):
                if row_number == 0:
                    column_count = len(row)
                    field_count.append(column_count) 
                    print("Number of fields/columns in this file is {}".format(column_count))
                total_num_of_rows += 1
                for column in row:
                    word = column.strip()
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1

    results['avg_num_of_fields'] = (sum(field_count) / len(field_count))
    results['total_num_of_rows'] = total_num_of_rows
    results['words'] = words
    return results

def output_word_count(word_count):
    output_filename = 'output.csv'
    header_row = ['value', 'count']
    with open(output_filename, 'w', encoding='utf-8') as output:
        writer = csv.writer(output,delimiter=',')
        writer.writerow(header_row)
        writer.writerows([[key, value] for key, value in word_count.items()])

def main():
    csv_list = get_csv_list()
    results = parse_csv_files(csv_list)
    print("Average number of fields across all .csv files: {}".format(results.get('avg_num_of_fields', 0)))
    output_word_count(results.get('words', {}))
    print("Total number of unique words across all .csv files: {}".format(len(results['words'].keys())))
    print("Total number of rows across all .csv files: {}".format(results.get('total_num_of_rows', 0)))

if __name__ == '__main__':
    main()