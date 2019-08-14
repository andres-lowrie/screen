from unittest import TestCase
from app.parser import Parser

TEST_FILES = [
    'test_data/1_csv/test_csv.csv',
    'test_data/2_csv/test_csv.csv',
    'test_data/2_csv/test2_csv.csv',
    'test_data/3_deep_csv/data/test3_csv.csv',
    'test_data/3_deep_csv/test_csv.csv',
    'test_data/3_deep_csv/test2_csv.csv'
]

class TestParser(TestCase):
    """Test that parser can parse."""

    def test_that_parser_can_be_created(self):
        """Can create parser object."""
        parser = Parser()
        self.assertIsNotNone(parser)

    def test_that_parser_can_scan(self):
       """Test that parser can parse csv."""
       parser = Parser(file_name=TEST_FILES[3])
       parser.parse()
       self.assertEqual(5, parser.fields())
       self.assertEqual(3, parser.count())
