from glob import iglob
from pathlib import Path
from collections import Counter
from csv import reader, DictWriter


def identify_delimiter(file_path):
   with open(str(file_path), 'r', encoding="utf-8", errors='ignore') as f:
      count = Counter(next(f))
      if ',' in count and ';' in count:
         return ',' if count[','] > count[';'] else ';'
      elif ';' in count:
         return ';'
      else:
         return ','


def count_occurrences(counts, csv_rows, row_count):
   for row in csv_rows:
      for value in row:
         value = value.strip('\n').strip()
         if not value or not value.isprintable():
            continue
         if value in counts:
            counts[value] += 1
         else:
            counts[value] = 1
         row_count += 1
   return counts, row_count


def write_results(counts):
   with open('results.csv', 'w', encoding='UTF-8', errors='ignore') as f:
      writer = DictWriter(f, fieldnames=['value', 'count'])
      writer.writerow({'value': 'value', 'count': 'count'})
      for value, count in counts.items():
         writer.writerow({'value': value, 'count': count})


def main():
   field_counts, file_count, row_count = 0, 0, 0
   value_counts = {}

   for file_path in iglob('../**/*.csv', recursive=True):
      delim = identify_delimiter(str(file_path))
      with open(str(file_path), 'r', encoding='UTF-8', newline='', errors='ignore') as f:
         csv_rows = reader(f, delimiter=delim)
         file_count += 1
         field_counts += len(next(csv_rows))
         value_counts, row_count = count_occurrences(value_counts, csv_rows, row_count)

   avg_fields = (field_counts/file_count) # Could use round() if we wanted.
   print("Average number of fields across csv files: {}".format(avg_fields))
   print("Total rows across csv files: {}".format(row_count))

   write_results(value_counts)


if __name__ == '__main__':
   main()
