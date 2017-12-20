#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang


import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_info = {
    'db_engine': 'file',
    'PATH': '%s/db' % BASE_DIR,
    'name': 'stuInfo.txt',
}

# LOG_LEVEL = logging.INFO
# LOG_TYPES = {
#     'transaction': 'transactions.log',
#     'access': 'access.log',
# }
