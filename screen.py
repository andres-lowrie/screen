# Python 3.7

import pathlib
import csv


TARGET_CVS = 'my_dataset.csv'


def get_list_of_cvs(folder: str = 'data', filename_extension: str = 'csv'):
    return sorted(pathlib.Path(folder).glob(f'**/*.{filename_extension}'))


def get_lines(file_name) -> int:
    lines = 0
    if file_name:
        with file_name.open('r', encoding='utf-8', errors='ignore') as target_file:
            lines = sum(1 for line in target_file)
        target_file.close()
    return lines


if __name__ == '__main__':
    print("Task 1:")
    list_of_cvs = get_list_of_cvs()
    total_lines = 0
    for item in list_of_cvs:
        total_lines = total_lines + get_lines(item)
    print(f" The average number of fields across all the .csv files: {total_lines // len(list_of_cvs)}")

    print("Task 2:")
    dict_list = {}
    for cvs_file in list_of_cvs:
        with cvs_file.open('r', encoding='utf-8', errors='ignore') as _data_cvs_file:
            reader = csv.reader(_data_cvs_file)
            for row in reader:
                for column in row:
                    target = column.strip()
                    if target in dict_list:
                        dict_list[target] = dict_list[target] + 1
                    else:
                        dict_list[target] = 1
        _data_cvs_file.close()

    title_row = ['value', 'count']
    with open(TARGET_CVS, 'w', encoding='utf-8') as target_cvs_file:
        writer = csv.writer(target_cvs_file, delimiter=',')
        writer.writerow(title_row)
        writer.writerows([[key, value] for key, value in dict_list.items()])
    target_cvs_file.close()
    print(" The task is done! Check my_dataset.csv")

    print("Task 3:")
    print(f" The total number of rows for the all the .cvs files :{total_lines}")
