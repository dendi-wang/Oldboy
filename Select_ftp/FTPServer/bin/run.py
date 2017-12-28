#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
from conf import settings
from core import Select_ftp

if __name__ == '__main__':
    ftpServer = Select_ftp.FTPServer()
    ftpServer.connent(settings.ip_port)
    ftpServer.interactive()
