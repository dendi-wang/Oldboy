#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import json

acc_dic = {
    'username': 'Harvey',
    'password': 'Harvey',
    'quota': 150000,
    'home': '/home/alex',
}


def add_user(acc_dic):
    file = 'account_files/%s.json' % acc_dic['username']
    f = open(file, 'w')
    f.write(json.dumps(acc_dic))


add_user(acc_dic)
