"""Scanner module."""

import os

EXTENTION = '.csv'

class Scanner:
    """
       Scanner that returns stats about
       input directory.
    """
    def __init__(self, input_dir='data'):
        """Constructor.
        """
        self.input_dir = input_dir 
        self.dirs = []

    def get_dir(self):
        """Name of directory to scan.
        """
        return self.input_dir

    def scan(self):
        """Run scanner.
        """
        for root, _, files in os.walk(self.input_dir):
            for name in files:
                if name.endswith(EXTENTION):
                    self.dirs.append(os.path.join(root, name))

    def files(self):
        """Get names of files.
        """
        return self.dirs
