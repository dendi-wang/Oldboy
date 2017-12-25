#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang






import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
from core.FabClass import FabClient

fabClient = FabClient('192.168.10.44', '22', 'root', 'redhat')
fabClient.exec_cmd('df')