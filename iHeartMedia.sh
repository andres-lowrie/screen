#!/bin/bash

find . -name "*.csv" > DOTcsvFiles.txt
python3 iheart_1.py
python3 iheart_2.py
python3 iheart_3.py
