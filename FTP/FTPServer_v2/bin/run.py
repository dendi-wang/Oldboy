#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import os
import sys
import socketserver

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
from core import FTPHandler

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 10000), FTPHandler.FTPHandler)
    server.serve_forever()
