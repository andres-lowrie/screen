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
        self.assertEqual(6, files_count)

    def test_rows_count(self):
        aggregator = Aggregator(input_dir='test_data')
        aggregator.aggregate()
        self.assertEqual(3.1667, aggregator.field_average())

    def test_average_fields(self):
        aggregator = Aggregator(input_dir='test_data')
        aggregator.aggregate()
        self.assertEqual(12, aggregator.total_count())
        
