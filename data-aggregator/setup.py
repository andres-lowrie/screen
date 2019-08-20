#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


MAIN_PACKAGE = 'data_aggregator'


class PyTest(TestCommand):

    user_options = [('cov-html=', None, 'Generate junit html report')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.cov = None
        self.pytest_args = ['--cov', MAIN_PACKAGE, '--cov-report', 'term-missing',
                            '--doctest-modules', '-s', '-v',
                            '--ignore', 'tests/data']
        self.cov_html = False

    def finalize_options(self):
        TestCommand.finalize_options(self)
        if self.cov_html:
            self.pytest_args.extend(['--cov-report', 'html'])

    def run_tests(self):
        try:
            import pytest
        except Exception:
            raise RuntimeError('py.test is not installed, run: pip install pytest')

        # HACK: circumvent strange atexit error with concurrent.futures
        # https://developer.blender.org/T39399
        # import concurrent.futures  # noqa

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def load_req(fn):
    return [r.strip() for r in open(fn).read().splitlines() if r.strip() and not r.strip().startswith('#')]


def enforce_py3():
    import sys
    major, *minor = sys.version_info
    if major < 3:
        raise RuntimeError('This package requires python 3')


if __name__ == '__main__':

    enforce_py3()

    # just in case setup.py is launched from elsewhere than the containing directory
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        cmdclass = {}
        cmdclass['test'] = PyTest

        setup(
            name='data-aggregator',
            version='0.1',
            description='Perform aggregations over csv files contained in github repositories owned by user datasets.',
            url='',
            license='Apache License 2.0',
            packages=find_packages(exclude=['tests', 'tests.*']),
            setup_requires=[],
            install_requires=load_req('requirements.txt'),
            cmdclass=cmdclass,
            test_suite='tests',
            tests_require=load_req('test_requirements.txt'),

            entry_points={
                'console_scripts': [
                    'data-aggregator = data_aggregator.aggregator:main',
                ]
            },
            include_package_data=True,  # (see MANIFEST.in)

            # more metadata for upload to PyPI
            author="Alfredo Valles Valdes",
            author_email="alfredo.valles@gmail.com",
            keywords='data aggregation csv',
            long_description=open('README.md').read(),
            classifiers=[
                'Development Status :: 5 - Production/Stable',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: Apache Software License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Topic :: Software Development :: Libraries :: Python Modules'],

            platforms='All',
        )

    finally:
        os.chdir(original_dir)
