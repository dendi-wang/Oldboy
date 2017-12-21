#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import json

acc_dic = {
    'username': 'alex',
    'password': 'alex',
    'quota': 15000,
    'home': '/home/alex',
}


def mod_acc(username, acc_dic):
    file = 'account_files/%s.json'
    f = open('account_files/alex.json', 'w')
    f.write(json.dumps(acc_dic))
