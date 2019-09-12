# Python 3.7

import pathlib
import csv
import chardet


TARGET_CVS = 'my_dataset.csv'


def get_list_of_csv(folder: str = 'data', filename_extension: str = 'csv') -> list:
    return sorted(pathlib.Path(folder).glob(f'**/*.{filename_extension}'))


def detect_encoding(file_name: pathlib.Path) -> dict:
    detector = chardet.UniversalDetector()
    with file_name.open('rb') as _file:
        for line in _file.readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        _file.close()
    return detector.result


def get_lines(file_name: pathlib.Path, encoding) -> int:
    lines = 0
    if file_name.stat().st_size > 0 and encoding is not None:
        with file_name.open('rt', encoding=encoding, errors='ignore') as target_file:
            lines = sum(1 for line in target_file)
        target_file.close()
    return lines


if __name__ == '__main__':
    print("Initial state:")
    list_of_csv = get_list_of_csv()

    print(" Detect encoding for each CSV file ...")
    files_dict = {}
    for csv_file in list_of_csv:
        files_dict[csv_file] = detect_encoding(csv_file)['encoding']

    print("Task 1:")
    total_lines = 0
    for csv_file, _encoding in files_dict.items():
        total_lines = total_lines + get_lines(csv_file, _encoding)
    print(f" The average number of fields across all the .csv files: {total_lines // len(list_of_csv)}")

    print("Task 2:")
    dict_list = {}
    for csv_file, _encoding in files_dict.items():
        if csv_file.stat().st_size > 0 and _encoding is not None:
            with csv_file.open('rt', encoding=_encoding, errors='ignore') as _data_cvs_file:
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
    with open(TARGET_CVS, 'wt', encoding='utf-8') as target_cvs_file:
        writer = csv.writer(target_cvs_file, delimiter=',')
        writer.writerow(title_row)
        writer.writerows([[key, value] for key, value in dict_list.items()])
    target_cvs_file.close()
    print(f" The task is done! Check {TARGET_CVS} file.")

    print("Task 3:")
    print(f" The total number of rows for the all the .cvs files: {total_lines}")
