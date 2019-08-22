#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import configparser
import logging

from collections import UserDict


from data_aggregator import settings
from data_aggregator.errors import FatalError


_config = None
_config_path = None
_config_parser = None


# def get_logger():
#     return logging.getLogger(__name__)


class _Config(UserDict):
    """
    Class for app configuration: A dict-like object that resolves key, value pairs from its internal data dict,
    or failing that from the config file, or failing that from the settings module.
    """

    def __init__(self, *args, **kwargs):
        self._parser = configparser.ConfigParser()
        self._config_access = dict()
        super().__init__(*args, **kwargs)

    def reset_config_parser(self, parser=None):
        self._parser = parser if parser else configparser.ConfigParser()
        self.data = dict()

    def set_access_list(self, access_dict):
        self._config_access = access_dict

    def __getitem__(self, key):

        if key in self.data:
            return self.data[key]

        if key in self._parser['DEFAULT']:  # get value from configfile
            if key not in self._config_access:
                raise FatalError('Forbidden: file config parameter: {} cannot override settings'.format(key))

            value = self._parser['DEFAULT'][key]
            val_type = self._config_access[key]
            try:
                # free form python expression evaluation
                if value and val_type == 'python_expression':
                    value = eval(value)
                # type conversions
                if value and val_type == 'int':
                    value = self._parser['DEFAULT'].getint(key)
                elif value and val_type == 'float':
                    value = self._parser['DEFAULT'].getfloat(key)
                elif value and val_type == 'bool':
                    value = self._parser['DEFAULT'].getboolean(key)
            except Exception as e:
                raise FatalError('Error evaluating config value: {}'.format(value)) from e
        elif hasattr(settings, str(key)):  # or get value from settings
            value = getattr(settings, str(key))
        else:
            raise KeyError('config key {} not found'.format(key))

        self.data[key] = value
        return self.data[key]

    def __contains__(self, key):
        return key in self.data or key in self._parser['DEFAULT'] or hasattr(settings, str(key))


def init_config(config_path=None):
    """Must be called once on app initialization"""

    global _config_path, _config_parser, _config

    _config_path = config_path
    _config_parser = configparser.ConfigParser()
    try:
        if config_path is not None:
            assert os.path.isfile(config_path), 'Config path {} is not a valid file path'.format(config_path)
        _config_parser.read(_config_path or '')
    except (AssertionError, OSError, configparser.Error) as e:
        # get_logger().exception('Could not parse App config file: %s. Details: ', config_path)
        raise FatalError('Failed to load config file: {}'.format(config_path)) from e
    else:
        _config = _Config()
        _config.reset_config_parser(_config_parser)
        _config.set_access_list(settings.config_access)


def get_config():
    """
    Get the app configuration: A dict-like object that resolves key, value pairs from its internal data dict,
    or failing that from the config file, or failing that from the settings module.
    """
    global _config
    if _config is None:
        _config = _Config()  # start empty config if not initialized
    return _config
