#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
import os, sys

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASEDIR)

sys.path.append(BASEDIR)

from core import main

if __name__ == '__main__':
    main.main()
