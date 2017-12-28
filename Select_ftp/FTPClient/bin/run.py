#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
from conf import settings
from core import FTPClient

if __name__ == '__main__':
    client = FTPClient.FtpClient()
    client.connent(('localhost', 10000))
    client.interactive()
