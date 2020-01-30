'''
main Python script for questions in screening process at iHeartMedia

Composed by: Parsa Yousefi (parsa.yousefi@utsa.edu)
'''

import os
import csv


def csv_finder(dir):  # this function finds only CSV files with their directories.
    csv_files = list()

    for root, dirs, files in sorted(os.walk(dir)):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    return csv_files


def average_field_counter(files):  # this function finds the average of fields in all CSV datasets.
    total_fields = 0

    for file in files:
        with open(file, 'r', encoding='latin-1') as f:
            csv_reader = csv.reader(f, dialect='excel')

            for row in csv_reader:
                total_fields += len(row)
                break

    return total_fields/len(files)


def word_counter(files):  # this function selects all values from all datasets with their count number.
    words_dict = {}

    for file in files:
        with open(file, 'r', encoding='latin-1') as f:
            csv_reader = csv.reader(f, dialect='excel')

            for row in csv_reader:
                for word in row:
                    if word != '':  # assuming not counting number of empty words
                        if word not in words_dict.keys():
                            words_dict[word] = 1

                        else:
                            words_dict[word] += 1

    return words_dict


def word_counts_saver(dict, output_path):  # this function saves the dictionary as a CSV file.
    with open(output_path, 'w', encoding='latin-1') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['value', 'count'])

        for key, value in dict.items():
            csv_writer.writerow([key, value])


def total_rows_counter(files):  # this function finds total number of rows in all datasets.
    total_rows = 0

    for file in files:
        with open(file, 'r', encoding='latin-1') as f:
            csv_reader = csv.reader(f, dialect='excel')

            for row in csv_reader:
                total_rows += 1

    return total_rows


if __name__ == '__main__':
    directory = './data'
    output_csv_file = './output_words_count.csv'

    csv_files_list = csv_finder(directory)

    average_fields = average_field_counter(csv_files_list)
    print('question 1: average value of of fields (columns) is {}'.format(average_fields))

    words_dictionary = word_counter(csv_files_list)
    word_counts_saver(words_dictionary, output_csv_file)
    print('question 2: dictionary of words with their counts has been saved in {}'.format(output_csv_file))

    total_rows = total_rows_counter(csv_files_list)
    print('question 3: total number of rows in all datasets is {}'.format(total_rows))
