"""Aggregator module.

"""
from csv import DictWriter
from collections import Counter

from app.scanner import Scanner
from app.parser import Parser

class Aggregator:
    """Class that gives statistics."""

    def __init__(self, input_dir=None, output_dir=None):
        """Constructor."""
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.scanner = Scanner(input_dir=input_dir)
        self.rows_count = 0
        self.fields = 0
        self.average_fields = 0
        self.file_count = 0
        self._word_counter = Counter() 

    def field_average(self):
        """Returns average number of fieilds.
        """
        return round(self.fields/self.file_count, 4) 

    def total_count(self):
        """Returns total count in all documents.
        """
        return self.rows_count 

    def aggregate(self):
        """Run aggragatins.
        """
        self.scanner.scan()
        self.file_count = self.scanner.files_count()
        for file in self.scanner.files():
            parser = Parser(file_name=file)
            parser.parse()
            self.rows_count += parser.count()
            self.fields += parser.fields()
            self._word_counter += parser.get_word_count()

    def files_count(self):
        """Returns number of scanned files.
        """
        return self.file_count 

    def word_count(self):
        """Total word count for all the files.
        """
        return self._word_counter

    def create_counts_file(self, file_name=None):
        """Create file with count of words.
        """
        header = ['value', 'count']
        with open(file_name, 'w') as csv_file:
            writer = DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            for value, count in self.word_count().items():
                writer.writerow({'value': value, 'count': count})
