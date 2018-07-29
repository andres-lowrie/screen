import process
from unittest import mock, TestCase


case3_csv_files = [['csv_file_abs_path\n']]


class ProcessTestCare(TestCase):

    def setUp(self):
        self.process = process
        self.process.write_word_count_csv = mock.MagicMock()
        self.process.glob.glob = mock.MagicMock()
        self.process.read_csv_file = mock.MagicMock()
        self.case1_csv_files = [['csv_file_abs_path']]
        self.case1_csv_data = [iter([['header1', 'header2'], ['word1', 'word2'], ['word1', 'word2'], ['word3', 'word4']])]
        self.case2_csv_files = [['csv_file_abs_path', 'csv_file_abs_path2']]
        self.case2_csv_data = [
            iter([['header1', 'header2'], ['word1', 'word2'], ['word1', 'word2'], ['word3', 'word4']]),
            iter([['header3', 'header4'], ['word1', 'word9'], ['word2', 'word2'], ['word30', 'word4']])
        ]

    def test_process_case1(self):
        self.process.glob.glob.side_effect = self.case1_csv_files
        self.process.read_csv_file.side_effect = self.case1_csv_data
        average_fields, total_rows, word_count = self.process.process()
        self.assertEqual(3, total_rows)
        self.assertEqual(2, word_count['word2'])
        self.assertEqual(2, average_fields)

    def test_process_case2(self):
        self.process.glob.glob.side_effect = self.case2_csv_files
        self.process.read_csv_file.side_effect = self.case2_csv_data
        average_fields, total_rows, word_count = self.process.process()
        self.assertEqual(6, total_rows)
        self.assertEqual(4, word_count['word2'])
        self.assertEqual(2, average_fields)

    def test_process_case3(self):
        self.process.glob.glob.side_effect = self.case1_csv_files
        self.process.read_csv_file.side_effect = self.case1_csv_data
        average_fields, total_rows, word_count = self.process.process()
        self.assertEqual(3, total_rows)
        self.assertEqual(2, word_count['word2'])
        self.assertEqual(2, average_fields)