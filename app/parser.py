"""Parser module."""

import csv

class Parser:
    """Class that parses csv files.
    """

    def __init__(self, file_name=None):
        """Construtor.
        """
        self.file_name = file_name
        self.header = ""
        self.document_count = 0

    def parse(self):
        """Parse csv.
        """
        with open(self.file_name, newline='\n') as csv_file:
           reader = csv.DictReader(csv_file)
           self.header = reader.fieldnames
           for row in reader:
               self.document_count += 1

    def count(self):
        """Return number of raws without the header.
        """
        return self.document_count

    def fields(self):
        """Return number of columns in the document.
        """
        return len(self.header)
