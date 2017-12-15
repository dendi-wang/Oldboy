#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
import os
from conf.settings import db_info
from core.db_handle import db_handle


def get_file_num():
    f_path = db_handle(db_info)
    file_num = os.listdir(f_path)[0].split('.')[0]
    return int(file_num)


