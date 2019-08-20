#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BaseError(Exception):
    """
    Base class of all known application exceptions
    """
    pass


class RecoverableError(BaseError):
    """
    Exception to raise in case of an error you can recover from
    """
    pass


class FatalError(BaseError):
    """
    Exception to raise for all fatal errors that we recognize and expect
    """
    pass
