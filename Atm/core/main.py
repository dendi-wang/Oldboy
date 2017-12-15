#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import json
import os
from conf import settings
from core import db_handle
from core import account
from core import logger


def main():
    print('欢迎登陆ATM。。。')
    print('''
    1.管理员登陆
    2.用户登陆
    ''')
    choice = input('请选择：')

    if choice == '1':
        manager_view()
    else:
        user_view()


def get_dic(acc_id):
    file_name = '%s.json' % str(acc_id)
    file_path = db_handle.db_handle(settings.db_info)
    acc_file = os.path.join(
        file_path, file_name
    )
    if os.path.exists(acc_file):
        with open(acc_file, 'r') as f:
            acc_dic = json.loads(f.readlines()[0])
        return acc_dic
    else:
        print('account is not exist...')
        return False


def withdraw(acc_id, acc_data):
    '''
    提现，手续费5%
    :param acc_data: 提现金额
    :return:
    '''
    acc_dic = get_dic(acc_id)
    balance = int(acc_dic['balance'])
    credit = int(acc_dic['credit'])
    if int(acc_data) <= balance:
        acc_dic['balance'] = int(balance) - int(acc_data)
        print('操作成功')
        message = '%s支出%s' % (acc_id, str(acc_data))
        logger.transaction_logger('%s支出%s' % (acc_id, str(acc_data)))
        account.mod_file(acc_id, acc_dic)
        logger.transaction_logger(message)
        return True
    elif int(acc_data) > balance and int(acc_data) <= balance + credit:
        acc_dic['balance'] = 0
        acc_dic['credit'] = credit - (int(acc_data) - int(balance))
        account.mod_file(acc_id, acc_dic)
        message = '%s支出%s' % (str(acc_id), str(acc_data))
        print('提现成功')
        logger.transaction_logger(message)
        return True
    else:
        message = '%s余额不足，无法提现。。。' % (acc_id,)
        print('余额不足，无法提现。。。')
        logger.transaction_logger(message)
        return False



def transfer_accounts(my_id, him_id, transfer_amount):
    '''
    转账
    :param account_id: 转账用户id
    :param acc_data: 转账金额
    :return:
    '''
    my_dic = get_dic(my_id)
    him_dic = get_dic(him_id)
    if int(transfer_amount) <= int(my_dic['balance']):
        my_dic['balance'] = int(my_dic['balance']) - int(transfer_amount)
        him_dic['balance'] = int(him_dic['balance']) + int(transfer_amount)
        account.mod_file(my_id, my_dic)
        account.mod_file(him_id, him_dic)
        print('转账成功。。。')
        message = '%s 向 %s转账%s' % (str(my_id), str(him_id), str(transfer_amount))
    else:
        message = '%s 向 %s转账失败,余额不足' % (str(my_id), str(him_id))
        print('余额不足转账失败')
    logger.transaction_logger(message)


def repay(acc_id, acc_data):
    '''
    还款
    :param acc_data:还款金额
    :return:
    '''
    acc_dic = get_dic(acc_id)
    if int(acc_dic['credit']) + int(acc_data) < 15000:
        acc_dic['credit'] = int(acc_dic['credit']) + int(acc_data)
    else:
        acc_dic['credit'] = 15000
    account.mod_file(acc_id, acc_dic)
    print('还款成功')
    message = '%s 还款 %s' % (str(acc_id), str(acc_data))
    logger.transaction_logger(message)

def auth(ismanager):
    def acc_auth(func):
        def wapper(*args, **kwargs):
            account_id = input('account_id: ')
            passwd = input('password: ')
            acc_dic = get_dic(account_id)
            if acc_dic != False:
                #print(acc_dic['id'], acc_dic['password'])
                if account_id == str(acc_dic['id']) and passwd == str(acc_dic['password']) :
                    if acc_dic['status'] == 0:
                        if ismanager == True and acc_dic['manager'] == "True":
                            func()
                        else:
                            func()
                    else:
                        print('User is freeze ....')
                else:
                    print('User has password  authentication')
            else:
                print('account is not exist...')
        return wapper
    return acc_auth


@auth(True)
def manager_view():
    '''
    manager_mune = {
        '1': add_user,
        '2': modity_limit,
        '3': freeze_user
    }
    '''
    while True:
        print('''
        1、添加用户
        2、修改额度
        3、冻结账号
        ''')
        choice = input('>>>')
        if choice.strip() == '1':
            userInfo = input('请输入用户信息（如："name=Harvey,password=123,manager=True"）>>>')
            account.add_user(userInfo)
        elif choice == '2':
            acc_id = input('请输入要修改的用户id:')
            new_limit = input('新的额度: ')
            account.modity_limit(acc_id, new_limit)
        elif choice == '3':
            acc_id = input('请输入要冻结的用户id:')
            account.freeze_user(acc_id)
        elif choice == 'q':
            exit('退出系统。。。')
        else:
            print('没有此操作')

@auth(False)
def user_view():
    while True:
        print('''
        1、还款
        2、转账
        3、提现或支付
        ''')
        choice = input('>>>')
        if choice == '1':
            acc_id = input('请输入账号ID：')
            acc_data = input('请输入还款金额：')
            repay(acc_id, acc_data)
        elif choice == '2':
            my_id = input('请输入自己的账户ID：')
            him_id = input('请输入转账账户：')
            transfer_amount = input('转账金额：')
            transfer_accounts(my_id, him_id, transfer_amount)
        elif choice == '3':
            acc_id = input('请输入账号ID：')
            acc_data = input('请输入提现金额：')
            withdraw(acc_id, acc_data)
        elif choice == 'q':
            exit('退出ATM')
        else:
            print('没有此操作。。。')
