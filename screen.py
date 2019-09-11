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


def is_exist_in_mydataset(_target):
    with open(TARGET_CVS, 'r', encoding='utf-8') as _mydataset_file:
        _reader = csv.reader(_mydataset_file)
        counter = 0
        for _row in _reader:
            if _row[0] == _target:
                _mydataset_file.close()
                return counter
            counter += 1
    _mydataset_file.close()
    return False


def add_in_mydataset(_target: str):
    with open(TARGET_CVS, 'a', encoding='utf-8') as _mydataset_file:
        target_data = [_target, 1]
        _writer = csv.writer(_mydataset_file, delimiter=',')
        _writer.writerow(target_data)
    _mydataset_file.close()


def increase_in_mydataset(_target, position):
    with open(TARGET_CVS, 'r', encoding='utf-8') as _mydataset_file:
        _reader = csv.reader(_mydataset_file)
        lines = list(_reader)

    lines[position][1] = int(lines[position][1]) + 1
    _mydataset_file.close()

    with open(TARGET_CVS, 'w', encoding='utf-8') as _target_cvs_file:
        _writer = csv.writer(_target_cvs_file, delimiter=',')
        _writer.writerows(lines)
    _target_cvs_file.close()


if __name__ == '__main__':
    print("Task 1:")
    # Searching all files
    list_of_cvs = get_list_of_cvs()

    total_lines = 0
    for item in list_of_cvs:
        total_lines = total_lines + get_lines(item)
    print(f" The average number of fields across all the .csv files: {total_lines // len(list_of_cvs)}")

    print("Task 2:")
    # Set initial state
    title_row = ['value', 'count']
    with open(TARGET_CVS, 'w', encoding='utf-8') as target_cvs_file:
        writer = csv.writer(target_cvs_file, delimiter=',')
        writer.writerow(title_row)
    target_cvs_file.close()

    for cvs_file in list_of_cvs:
        with cvs_file.open('r', encoding='utf-8', errors='ignore') as _data_cvs_file:
            reader = csv.reader(_data_cvs_file)
            for row in reader:
                for column in row:
                    check = is_exist_in_mydataset(column)
                    if check:
                        increase_in_mydataset(column, check)
                    else:
                        add_in_mydataset(column)
        _data_cvs_file.close()
    print(" The task is done! Check my_dataset.csv")

    print("Task 3:")
    print(f" The total number of rows for the all the .cvs files :{total_lines}")
