#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import json

acc_dic = {
    'id': 1234,
    'password': 'abc',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2016-01-02',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 0,  # 0 = normal, 1 = locked, 2 = disabled
    'manager': True  # 是否是管理员
}

print(json.dumps(acc_dic))
