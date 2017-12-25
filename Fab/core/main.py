#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from core.FabClass import FabClient
from conf import settings


# print(type(settings.HOSTS))

def interactive():
    for k, v in settings.HOSTS.items():
        print(k)
        for i, j in v.items():
            print(i, j)


interactive()
