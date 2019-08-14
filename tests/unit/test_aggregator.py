import os
import filecmp

from unittest import TestCase

from app.aggregator import Aggregator

class TestAggregator(TestCase):
    """Testing aggregator class."""

    def test_aggregator_is_created(self):
        aggregator = Aggregator()
        self.assertIsNotNone(aggregator)

    def test_average_number_of_fields(self):
        aggregator = Aggregator()
        with self.assertRaises(ZeroDivisionError):
            aggregator.field_average()

    def test_total_number_of_rows(self):
        aggregator = Aggregator()
        self.assertEqual(0, aggregator.total_count())

    def test_file_count(self):
        aggregator = Aggregator(input_dir='test_data')
        aggregator.aggregate()
        files_count = aggregator.files_count()
        self.assertEqual(7, files_count)

    def test_rows_count(self):
        aggregator = Aggregator(input_dir='test_data')
        aggregator.aggregate()
        self.assertEqual(2.7143, aggregator.field_average())

    def test_average_fields(self):
        aggregator = Aggregator(input_dir='test_data')
        aggregator.aggregate()
        self.assertEqual(12, aggregator.total_count())

    def test_aggregator_counter(self):
        aggregator = Aggregator(input_dir='test_data')
        aggregator.aggregate()
        self.assertEqual(
            {'2019-01-01': 3, 'USA': 1, 'Ukraine': 1, 'Mexico': 1}, 
            aggregator.word_count()
        )

    def test_csv_output(self):
        test_file = 'test.csv'
        test_output = 'tmp.csv'
        aggregator = Aggregator(input_dir='test_data')
        aggregator.aggregate()
        aggregator.create_counts_file(file_name=test_output)
        self.assertTrue(filecmp.cmp(test_file, test_output))
        os.remove(test_output)
