from unittest import TestCase
from app.scanner import Scanner

TEST_FILES = [
    'test_data/1_csv/test_csv.csv',
    'test_data/2_csv/test_csv.csv',
    'test_data/2_csv/test2_csv.csv',
    'test_data/3_deep_csv/data/test3_csv.csv',
    'test_data/3_deep_csv/test_csv.csv',
    'test_data/3_deep_csv/test2_csv.csv'
]

class TestScanner(TestCase):
    """Test for scanner class.
    """
    def setUp(self):
        self.scanner = Scanner(input_dir='test_data')

    def test_that_scanner_exists(self):
        """Check that scanner created.
        """
        self.assertIsNotNone(self.scanner)
        self.assertEqual('test_data', self.scanner.get_dir())

    def test_scanner_knows_what_to_scann(self):
        """Check that scanner remembers 
           directory to scan.
        """
        self.assertEqual('test_data', self.scanner.get_dir())

    def test_that_scanner_can_scan(self):
        """Test that scanner can find .csv files.
        """
        self.scanner.scan()

        self.assertEqual(
            sorted(TEST_FILES), 
            sorted(self.scanner.files())
        )
