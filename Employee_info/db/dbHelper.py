#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import os
from conf import settings

db_type = settings.db_info['db_engine']


def dbHeler(db_type='file', *args, **kwargs):
    if db_type == 'file':
        db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sheet\staff_table.txt')
        table_field = {
            'id': 0,
            'name': 1,
            'age': 2,
            'phone': 3,
            'dept': 4,
            'enroll_date': 5
        }
        return db_file, table_field
    elif db_type == 'mysql':
        pass

    else:
        pass


# print(dbHeler(db_type))
