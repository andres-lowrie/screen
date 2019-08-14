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

    def test_that_parser_gets_words(self):
       parser = Parser(file_name=TEST_FILES[3])
       parser.parse()
       self.assertEqual(
           ['USA', 'Ukraine', 'Mexico'],
           parser.get_words()
       )


    def test_word_counter(self):
       parser = Parser(file_name=TEST_FILES[3])
       parser.parse()
       self.assertEqual(
           {'USA': 1, 'Ukraine': 1, 'Mexico': 1},
           parser.get_word_count()
       )

    def test_word_counter_again(self):
       parser = Parser(file_name=TEST_FILES[1])
       parser.parse()
       self.assertEqual(
           {'2019-01-01': 1},
           parser.get_word_count()
       )

    def test_that_parser_gets_words_again(self):
       parser = Parser(file_name=TEST_FILES[1])
       parser.parse()
       self.assertEqual(
           ['2019-01-01'],
           parser.get_words()
       )

    def test_that_parser_can_scan_again(self):
       """Test that parser can parse csv."""
       parser = Parser(file_name=TEST_FILES[1])
       parser.parse()
       self.assertEqual(2, parser.fields())
       self.assertEqual(1, parser.count())
