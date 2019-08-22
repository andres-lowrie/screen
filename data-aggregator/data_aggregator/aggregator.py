#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perform aggregations over csv files contained in github repositories owned by user datasets.

Our official repo: https://github.com/andres-lowrie/screen
Datasets repo: https://github.com/datasets
"""

import sys
import os
import csv
import re
import argparse
import logging

from collections import Counter

from data_aggregator.errors import RecoverableError, FatalError
from data_aggregator.config import init_config, get_config


#################################################################
# Global parameters that control default behaviour

# DATA_DIR = '/root/data'
# OUTPUT_DIR = '/root/output'
#
# OUTPUT_AVG_FIELDS_FILE = 'question1_avg_fields.txt'
# OUTPUT_COUNT_FILE = 'question2_aggregated_counts.csv'
# OUTPUT_TOTAL_ROWS = 'question3_total_rows.txt'
#
# OUTPUT_PARSE_FAILURE = 'csv_files_parse_failure.txt'
# OUTPUT_PARSE_SUCCESS = 'csv_files_parse_success.txt'
# OUTPUT_LOG = 'app-logfile.log'
#
# SEARCH_FILE_PATTERN = r'.+\.csv$'
# INPUT_ENC = 'utf-8'
# OUTPUT_ENC = 'utf-8'
#
# LOG_DISABLED = False  # disables all logging
# LOG_LEVEL = 'INFO'
# LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'

# End Global parameters
#################################################################


_logger = None
_paths_parse_failure = []
_paths_parse_success = []


def get_logger():
    return logging.getLogger(__name__)


def _init_logger(filename=None, level=None):
    global _logger

    if not _logger:
        config = get_config()
        filename = filename or os.path.join(config['OUTPUT_DIR'], config['OUTPUT_LOG'])
        level = level or config['LOG_LEVEL']
        if config['LOG_DISABLED']:
            logging.disable(logging.CRITICAL)  # disable all logging output
        else:
            level = getattr(logging, level)
            logging.basicConfig(filename=filename, level=level, format=config['LOG_FORMAT'], filemode='a')

        _logger = logging.getLogger(__name__)
    return _logger


def _init_output_folder():
    """creates output dir if does not exist"""
    config = get_config()
    path = config['OUTPUT_DIR']
    try:
        os.makedirs(path, mode=0o755, exist_ok=True)
    except OSError as e:
        raise FatalError('Aborting: Could not create output dir {}. Reason: {}'.format(path, e)) from e


def init_app(args):
    """Must be called in the beginning of the app execution"""
    init_config(args.config_file)
    _init_output_folder()
    _init_logger()


class FileMatchIterable:
    """
    Container class that provide reusable iteration over file names that match a pattern inside a directory.
    This pattern is more general and safer than  a generator function.
    """

    def __init__(self, root_dir, regex=r'.+\.csv$'):
        self.root_dir = root_dir
        self.pattern = None
        self._creg = None
        self.set_pattern(regex)

    def set_pattern(self, regex):
        self.pattern = regex
        self._creg = re.compile(regex, re.IGNORECASE | re.UNICODE)

    def __iter__(self):
        """Iterator produce filepaths that match the pattern under root_dir."""
        root_dir = os.path.abspath(os.path.expanduser(self.root_dir))
        try:
            for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True, followlinks=False):
                for filename in filenames:
                    if self._creg.match(filename):
                        yield os.path.join(dirpath, filename)
        except OSError as e:
            get_logger().exception('IO Error while recursively searching dir %s. Details: ', self.root_dir)
            raise FatalError('IO Error while recursively searching dir {}'.format(self.root_dir)) from e


class CsvAggregator:
    """Class to parse a csv file and maintain simple value counts"""

    def __init__(self, path_to_file, encoding=None, sniff_bytes=65536):
        self.path = path_to_file
        self.encoding = get_config()['INPUT_ENC'] if not encoding else encoding
        self.sniff_bytes = sniff_bytes
        self.fields = []
        self.num_rows = 0
        self.counter = Counter()

        self.filep = None
        self.csv_sniffer = None
        self.csv_dialect = None
        self.csv_has_header = False
        self.csv_reader = None

        self._init_csv()

    def _open_file(self):
        get_logger().info('opening csv: %s', self.path)
        self.filep = open(self.path, 'r', encoding=self.encoding, newline='')

    def _detect_csv_dialect(self):
        self.csv_sniffer = csv.Sniffer()

        sample = self.filep.read(self.sniff_bytes)
        self.filep.seek(0)

        self.csv_dialect = self.csv_sniffer.sniff(sample)
        self.csv_has_header = self.csv_sniffer.has_header(sample)

        if self.csv_has_header:
            get_logger().info('csv sniffer for file %s: has_header=%s', self.path, self.csv_has_header)
        else:
            get_logger().warning('Rejecting csv with no headers %s', self.path)
            raise RecoverableError('Cannot process csv {} without recognized headers'.format(self.path))

    def _create_csv_reader(self):
        reader_clazz = csv.DictReader if self.csv_has_header else csv.reader
        self.csv_reader = reader_clazz(self.filep, dialect=self.csv_dialect)
        get_logger().info('csv reader created for file: %s', self.path)

    def _init_csv(self):
        try:
            self._open_file()
            self._detect_csv_dialect()
            self._create_csv_reader()
        except OSError as e:
            get_logger().exception('IO Error while opening file %s. Details: ', self.path)
            raise FatalError('IO Error while opening file {}'.format(self.path)) from e
        except csv.Error as e:
            get_logger().exception('CSV Parse Error on file %s. Details: ', self.path)
            raise RecoverableError('CSV parser error on init') from e
        except UnicodeDecodeError as e:
            get_logger().exception('Encoding Error on file %s. Details: ', self.path)
            raise RecoverableError('Encoding Error on file {}'.format(self.path)) from e

    def process(self):
        try:

            for i, record in enumerate(self.csv_reader):

                if self.csv_has_header:
                    if i == 0:  # save csv headers
                        self.fields = list(record.keys())
                    else:
                        if len(record) != len(self.fields):
                            get_logger().error('Error-ID:534: Line != fields. File %s, line: %s', self.path, i + 1)
                            raise RecoverableError('CSV file {} parse error in line {}'.format(self.path, i + 1))

                    self._process_dict_record(record, i + 1)
                else:
                    self._process_list_record(record, i + 1)

        except csv.Error as e:
            get_logger().exception('CSV Error on file %s. Details: ', self.path)
            raise RecoverableError('CSV parser error') from e
        except UnicodeDecodeError as e:
            get_logger().exception('Encoding Error on file %s. Details: ', self.path)
            raise RecoverableError('Encoding Error on file {}'.format(self.path)) from e

    def _process_dict_record(self, record, line_num):
        try:
            self.counter.update(record.values())
        except TypeError as e:
            # catch: TypeError: unhashable type: 'list'
            get_logger().exception('Error-ID:535: csv file: %s, parse error in line: %s', self.path, line_num)
            raise RecoverableError("csv file {}: unhashable 'list' in line: {}".format(self.path, line_num)) from e

        self.num_rows += 1

    def _process_list_record(self, record, line_num):
        raise NotImplementedError('Can not process csv {} without recognized headers'.format(self.path))


class StatsAggregator:
    """Class to compute simple stats by aggregating the results of CsvAggregator instances"""

    def __init__(self):
        self.total_files = 0  # number of files seen
        self.total_rows = 0  # sum of rows in all files seen
        self.total_fields = 0  # sum of fields in all files seen
        self.counter = Counter()  # count of repeated values in all files seen

    @property
    def average_fields(self):
        try:
            return self.total_fields / self.total_files
        except ZeroDivisionError:
            return float('NaN')

    @property
    def average_rows(self):
        try:
            return self.total_rows / self.total_files
        except ZeroDivisionError:
            return float('NaN')

    def add_partial(self, csv_aggregator):
        self.total_files += 1
        self.total_fields += len(csv_aggregator.fields)
        self.total_rows += csv_aggregator.num_rows
        self.counter.update(csv_aggregator.counter)

    def save_count_to_csv(self, file_path, limit=None):

        fieldnames = ['value', 'count']

        with open(file_path, 'w', encoding=get_config()['OUTPUT_ENC'], newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for value_count in self.counter.most_common(n=limit):
                csv_record = dict(zip(fieldnames, value_count))
                writer.writerow(csv_record)  # writer.writerow({'value': 'one_value', 'count': 5})


def _save_paths_parsed(paths_list, filename=None):
    output_path = os.path.join(get_config()['OUTPUT_DIR'], filename or get_config()['OUTPUT_PARSE_FAILURE'])
    try:
        with open(output_path, 'w', encoding=get_config()['OUTPUT_ENC']) as f:
            f.write('\n'.join(paths_list))
    except OSError as e:
        get_logger().warning('Could not save parsed csv list to file: %s. Details: %s', output_path, e)


def save_results(stats):
    """Simple persistence for the results obtained"""

    config = get_config()
    try:
        # question 1: average number of fields across cvs files
        output_path = os.path.join(config['OUTPUT_DIR'], config['OUTPUT_AVG_FIELDS_FILE'])
        with open(output_path, 'w', encoding=config['OUTPUT_ENC']) as fp:
            fp.write('{}'.format(stats.average_fields))

        get_logger().info('question1 (average_fields) result: %s, saved to %s', stats.average_fields, output_path)

        # question 2
        output_path = os.path.join(config['OUTPUT_DIR'], config['OUTPUT_COUNT_FILE'])
        stats.save_count_to_csv(output_path)

        get_logger().info('question2 (value_counts) saved to %s', output_path)

        # question 3
        output_path = os.path.join(config['OUTPUT_DIR'], config['OUTPUT_TOTAL_ROWS'])
        with open(output_path, 'w', encoding=config['OUTPUT_ENC']) as fp:
            fp.write('{}'.format(stats.total_rows))

        get_logger().info('question3 (total_rows) result: %s, saved to %s', stats.total_rows, output_path)

    except OSError as e:
        get_logger().exception('IO Error while saving results. Details:')
        raise FatalError('IO Error while saving results') from e
    else:
        get_logger().info('Saving results completed successfully')


def process_all():
    """Performs most of the application logic"""

    config = get_config()
    try:
        paths_matched = FileMatchIterable(config['DATA_DIR'], regex=config['SEARCH_FILE_PATTERN'])

        stats_agg = StatsAggregator()

        for csv_path in paths_matched:

            try:
                csv_agg = CsvAggregator(csv_path)
                csv_agg.process()

                stats_agg.add_partial(csv_agg)

            except RecoverableError:
                get_logger().exception('Skipping csv %s due to Recoverable error. Details: ', csv_path)
                _paths_parse_failure.append(csv_path)
            else:
                _paths_parse_success.append(csv_path)
                get_logger().info('csv file %s processed successfully <<<')

        get_logger().info('CSV parsing completed: num_included=%s, num_failed=%s', len(_paths_parse_success),
                          len(_paths_parse_failure))
        print('CSV parsing completed: successes={}, failed={}'.format(len(_paths_parse_success),
                                                                      len(_paths_parse_failure)))

        save_results(stats_agg)

    except FatalError:
        get_logger().exception('Fatal error: ')
        raise
    finally:
        # save current list of csv processed and failed
        _save_paths_parsed(_paths_parse_success, filename=config['OUTPUT_PARSE_SUCCESS'])
        _save_paths_parsed(_paths_parse_failure, filename=config['OUTPUT_PARSE_FAILURE'])


def parse_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    parser.add_argument('-c', '--config-file', default=None, help='')
    return parser.parse_args()


def main():
    """Entry point for installed package command"""

    try:
        args = parse_args()

        init_app(args)

        get_logger().info('Starting new execution')

        process_all()

    except FatalError as e:
        get_logger().exception('Exiting program due to fatal error:')
        print('Exiting program due to fatal error: {}'.format(e), file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        get_logger().exception('Unhandled exception reached top level: ')
        print('Exiting program: Unhandled exception reached top level: {}'.format(e), file=sys.stderr)
        sys.exit(5)


if __name__ == '__main__':
    main()
