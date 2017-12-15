#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
from core import main


def acc_auth(func):
    def wapper(ismanager):
        account_id = input('account_id: ')
        passwd = input('password: ')
        acc_dic = main.get_dic(account_id)
        if account_id == acc_dic['id'] and passwd == acc_dic['password'] and ismanager == acc_dic['manager']:
            if acc_dic['status'] == 0:
                func()
            else:
                print('User is freeze ....')
        else:
            func()
            print('User has password  authentication')

    return wapper
