from glob import iglob
from pathlib import Path
from collections import Counter
from csv import reader, DictWriter


def identify_delimiter(file_path):
   """ Read in the first line of the file and determine the delimiter type.

   We read in the first line and do a Counter of all characters. Then determine
   which of the two is most likely to be the delimiter and return that back.

   :param str file_path: The path of the csv file we are going to examine.
   :return: The delimiter we will be using to examine the rest of the file.
   :rtype: str
   """
   with open(str(file_path), 'r', encoding="utf-8", errors='ignore') as f:
      count = Counter(next(f))
      if ',' in count and ';' in count:
         return ',' if count[','] > count[';'] else ';'
      elif ';' in count:
         return ';'
      else:
         return ','


def count_occurrences(counts, csv_rows, row_count):
   """ Count the occurrences of each value field and return the results.

   Here we look through each value and map it to the number of times we have
   seen it. If it is the first time we encounter the value, we set it to 1. If
   this is not, we add a 1 to the running total.

   :param dict counts: A dictionary with the keys as column values and the
                       value as the number of times we have seen the key so
                       far.
   :param iter csv_rows: The output from csv.reader. An iterable object.
   :param int row_count: Running total of the number of rows we have
                         encountered thus far.
   :return: A tuple containing both the counts of occurrences and the running
            total of encountered rows
   :rtype: dict, int
   """
   for row in csv_rows:
      for value in row:
         # Remove leading and trailing whitespace as well as newlines.
         value = value.strip('\n').strip()
         # Determine if it is an empty value or if its an invisible character.
         # If so, lets move on to the next value and discard this one.
         if not value or not value.isprintable():
            continue
         if value in counts:
            counts[value] += 1
         else:
            counts[value] = 1
         row_count += 1
   return counts, row_count


def write_results(counts):
   """ Write the value occurrence results to a file called results.csv

   :param dict counts: A dictionary with the keys as column values and the
                       value as the number of times we have seen the key so
                       far.
   """
   with open('results.csv', 'w', encoding='UTF-8', errors='ignore') as f:
      writer = DictWriter(f, fieldnames=['value', 'count'])
      writer.writerow({'value': 'value', 'count': 'count'})

      for value, count in counts.items():
         writer.writerow({'value': value, 'count': count})


def main():
   field_counts, file_count, row_count = 0, 0, 0
   value_counts = {}

   # Recursively search the parent directory for all csv files
   for file_path in iglob('../**/*.csv', recursive=True):
      # Figure out which delimiter we want to use to examine the file.
      delim = identify_delimiter(str(file_path))

      with open(str(file_path), 'r', encoding='UTF-8', newline='', errors='ignore') as f:
         csv_rows = reader(f, delimiter=delim)

         # This will keep track of how many files we've opened for avg field
         # count
         file_count += 1

         # Extract the header of the csv file and add the number of fields to
         # the running total.
         field_counts += len(next(csv_rows))

         # Get number of occurences of each column value. While we are at it,
         # might as well also get the running total rows of all csv files. Keep
         # in mind, we purposely omit each csv file header from the count.
         value_counts, row_count = count_occurrences(value_counts, csv_rows, row_count)

   avg_fields = (field_counts/file_count) # Could use round() if we wanted.

   print("Average number of fields across csv files: {}".format(avg_fields))
   print("Total rows across csv files: {}".format(row_count))
   write_results(value_counts)


if __name__ == '__main__':
   main()
