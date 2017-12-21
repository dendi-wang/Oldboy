#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
import os

IP_PORT = ('localhost', 10000)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = '%s/db/account_files' % BASE_DIR

path_separator = '\\'

print(BASE_DIR)
