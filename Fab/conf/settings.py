#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
import os
import platform

IP_PORT = ('localhost', 10000)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

download_path = '%s/download/' % BASE_DIR

HOSTS = {
    'test': {
        1: ['192.168.10.44', 22, 'root', 'redhat'],
        2: ['192.168.10.220', 22, 'game', 'a123456!']
    },

    'boss': {
        1: ['192.168.10.159', 22, 'game', 'Playmore123!'],
        2: ['192.168.10.185', 22, 'game', 'Playmore123!']
    },
}



# plat = platform.system()
# if plat == 'Windows':
#     path_separator = '\\'
# else:
#     path_separator = '/'
