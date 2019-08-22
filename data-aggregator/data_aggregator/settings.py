#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################################################
# Default values for the settings that control app behaviour
# Can be overridden in the config

DATA_DIR = '/root/data'
OUTPUT_DIR = '/root/output'

OUTPUT_AVG_FIELDS_FILE = 'question1_avg_fields.txt'
OUTPUT_COUNT_FILE = 'question2_aggregated_counts.csv'
OUTPUT_TOTAL_ROWS = 'question3_total_rows.txt'

OUTPUT_PARSE_FAILURE = 'csv_files_parse_failure.txt'
OUTPUT_PARSE_SUCCESS = 'csv_files_parse_success.txt'
OUTPUT_LOG = 'app-logfile.log'

SEARCH_FILE_PATTERN = r'.+\.csv$'
INPUT_ENC = 'utf-8'
OUTPUT_ENC = 'utf-8'

LOG_DISABLED = False  # disables all logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'

# End default settings
#################################################################


# Defines which parameters can be overridden in the configuration file

config_access = dict([
    ('DATA_DIR', 'str'),
    ('OUTPUT_DIR', 'str'),

    ('OUTPUT_AVG_FIELDS_FILE', 'str'),
    ('OUTPUT_COUNT_FILE', 'str'),
    ('OUTPUT_TOTAL_ROWS', 'str'),

    ('OUTPUT_PARSE_FAILURE', 'str'),
    ('OUTPUT_PARSE_SUCCESS', 'str'),
    ('OUTPUT_LOG', 'str'),

    ('SEARCH_FILE_PATTERN', 'str'),
    ('INPUT_ENC', 'str'),
    ('OUTPUT_ENC', 'str'),

    ('LOG_DISABLED', 'bool'),
    ('LOG_LEVEL', 'str'),
    ('LOG_FORMAT', 'str'),
])