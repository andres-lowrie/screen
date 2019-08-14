"""Parser module."""

import csv
import logging
from collections import Counter
from app.utils import parse_with_type

class Parser:
    """Class that parses csv files.
    """

    def __init__(self, file_name=None):
        """Construtor.
        """
        self.file_name = file_name
        self.header = ""
        self.document_count = 0
        self.words = []

    def parse(self):
        """Parse csv.
        """
        with open(self.file_name, encoding='latin1') as csv_file:
           logging.info(f"Parsing file {self.file_name}")
           reader = csv.DictReader(csv_file)
           self.header = reader.fieldnames
           for row in reader:
               self.document_count += 1
               for header in self.header:
                   _type, value = parse_with_type(row[header])
                   if _type == str: 
                       self.words.append(row[header])

    def count(self):
        """Return number of raws without the header.
        """
        return self.document_count

    def fields(self):
        """Return number of columns in the document.
        """
        if self.header is None: return 0
        return len(self.header)

    def get_words(self):
        """Returns list of parsed words.
        """
        return self.words

    def get_word_count(self):
        """Returns counter of all the words.
        """
        return Counter(self.words)
