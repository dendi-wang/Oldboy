#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
import os
import platform

IP_PORT = ('localhost', 10000)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

download_path = '%s/download/' % BASE_DIR

# plat = platform.system()
# if plat == 'Windows':
#     path_separator = '\\'
# else:
#     path_separator = '/'
