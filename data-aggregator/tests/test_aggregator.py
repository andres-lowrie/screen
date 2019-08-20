#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
import sys
from itertools import chain
from random import shuffle
import io
from collections import defaultdict
import logging


from data_aggregator.aggregator import FileMatchIterable
from data_aggregator.aggregator import CsvAggregator
from data_aggregator.aggregator import StatsAggregator


def get_logger():
    return logging.getLogger(__name__)


def test_file_finder():

    data_dir = os.path.join(os.path.dirname(__file__), 'data')

    file_finder = FileMatchIterable(data_dir)

    filepaths = list(file_finder)

    # check paths are absolute
    assert len([path for path in filepaths if os.path.isabs(path)]) == len(filepaths)

    # check file1 and file2 are in there
    most_include_basenames = ['file1.csv', 'file2.csv']

    assert len([1 for path in filepaths if os.path.basename(path) in  most_include_basenames]) == \
           len(most_include_basenames)


def quick_parse_csv(path, sep=','):
    """Auxiliary function to quickly parse a simple csv with header"""

    parsed = dict()

    parsed['lines'] = open(path, 'r').readlines()
    parsed['header'] = parsed['lines'][0].strip()
    parsed['data'] = parsed['lines'][1:]
    parsed['columns'] = [col.strip() for col in parsed['header'].split(sep)]

    # quick count of file1.csv values
    my_count = defaultdict(int)
    for line in parsed['data']:
        values = line.strip().split(sep)
        for v in values:
            my_count[v] += 1
    parsed['my_count'] = my_count
    return parsed



def test_csv_aggregator():

    data_dir = os.path.join(os.path.dirname(__file__), 'data')

    path1 = os.path.join(data_dir, 'file1.csv')

    csv_agg = CsvAggregator(path1)

    csv_agg.process()

    # check that the header presence was detected
    assert csv_agg.csv_has_header == True

    # our quick and dirty parsing of csv
    csv_parsed = quick_parse_csv(path1)

    # check that all the fields (columns) are recognized
    assert set(csv_agg.fields) == set(csv_parsed['columns'])

    # check number of rows
    assert csv_agg.num_rows == len(csv_parsed['data'])

    # check values counter is correct
    value_count_list = csv_agg.counter.most_common()
    assert set(value_count_list) == set(csv_parsed['my_count'].items())


def test_stats_aggregator():

    data_dir = os.path.join(os.path.dirname(__file__), 'data')

    path1 = os.path.join(data_dir, 'file1.csv')

    # let's process the same file several times and aggregate the stats
    n = 10

    stats_agg = StatsAggregator()

    for _ in range(n):
        csv_agg = CsvAggregator(path1)
        csv_agg.process()

        stats_agg.add_partial(csv_agg)

    # check number of processed files
    assert stats_agg.total_files == n

    # quick and dirty parsing of csv
    csv_parsed = quick_parse_csv(path1)

    # check the accumulation of all rows is ok
    assert stats_agg.total_rows == len(csv_parsed['data']) * n

    # check that the accumulation of fields is ok
    assert stats_agg.total_fields == len(csv_parsed['columns']) * n

    # check that the accumulated counter is ok
    assert set(stats_agg.counter.most_common()) == set([(val, count * n) for val, count in
                                                        csv_parsed['my_count'].items()])

    # TODO: test saving the counts to a csv file
