#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
import logging


from data_aggregator.config import init_config, get_config
from data_aggregator import settings
from data_aggregator.errors import FatalError


def get_logger():
    return logging.getLogger(__name__)


@pytest.fixture(scope='module')
def data_dir():
    return os.path.join(os.path.dirname(__file__), 'data')


def test_config_loading(monkeypatch, data_dir):

    # Mocks:
    mock_config_access = dict(settings.config_access)
    mock_config_access['SOME_FANCY_EXPRESSION'] = 'python_expression'  # add SOME_FANCY_EXPRESSION to app settings
    # mock_config_access['LOG_DISABLED'] = None  # disables boolean type conversion: uncomment to trigger error
    monkeypatch.setattr(settings, 'config_access', mock_config_access)

    monkeypatch.setattr(settings, 'LOG_DISABLED', False)  # We be read from the config file as True
    monkeypatch.setattr(settings, 'SOME_FANCY_EXPRESSION', 1, raising=False)
    monkeypatch.setattr(settings, 'KEY_IN_SETTINGS_BUT_NOT_IN_CONFIG', 2, raising=False)


    config_path = os.path.join(data_dir, 'app_test_config.ini')

    init_config(config_path)

    config = get_config()

    # test that we can read values from the config file
    assert config['DATA_DIR'] == '/for/test/only'

    # test the boolean type conversion
    assert config['LOG_DISABLED'] is True, 'boolean type conversion failed'

    # test dict contains
    assert 'DATA_DIR' in config  # key in UserDict.data
    assert 'OUTPUT_LOG' in config  # key in configparser
    assert 'LOG_FORMAT' in config  # key in settings
    assert 'KEY_IN_SETTINGS_BUT_NOT_IN_CONFIG' in config  # key in settings but not declared in config_access

    # test loading key from settings
    assert config['LOG_FORMAT'] == settings.LOG_FORMAT

    # test loading key from settings that is not declared in config_access
    assert config['KEY_IN_SETTINGS_BUT_NOT_IN_CONFIG'] == getattr(settings, 'KEY_IN_SETTINGS_BUT_NOT_IN_CONFIG')

    # test loading key from config file marked as a python expression
    assert config['SOME_FANCY_EXPRESSION'] == {'fancy', 'python', 'expression'}

    # test loading key from config file raises error if key not marked for override in settings.config_access
    with pytest.raises(FatalError, match=r'^Forbidden: file config parameter: NOT_IN_SETTINGS .*'):
        _ = config['NOT_IN_SETTINGS']

    # test loading an unknown key not present anywhere raises KeyError
    with pytest.raises(KeyError):
        _ = config['UNKNOWN_KEY_123']

    monkeypatch.undo()


def test_config_loading_no_file(monkeypatch):

    init_config(config_path=None)  # No config file

    config = get_config()

    # Mocks:
    # mock_config_access = dict(settings.config_access)
    # mock_config_access['SOME_FANCY_EXPRESSION'] = 'python_expression'  # add SOME_FANCY_EXPRESSION to app settings
    # monkeypatch.setattr(settings, 'config_access', mock_config_access)

    monkeypatch.setattr(settings, 'LOG_DISABLED', False)  # We be read from the config file as True
    monkeypatch.setattr(settings, 'SOME_FANCY_EXPRESSION', 1, raising=False)

    # test that we can access the default values in settings

    assert config['LOG_DISABLED'] is False
    assert config['SOME_FANCY_EXPRESSION'] == 1

    monkeypatch.undo()
