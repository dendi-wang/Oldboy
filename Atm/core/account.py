#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

from conf import settings
from core import db_handle
from db import dbrecord
from core import main
import json, os, time, datetime


def mod_file(acc_id, *args):
    #print(args)
    file_name = '%s.json' % str(acc_id)
    file_path = db_handle.db_handle(settings.db_info)
    acc_file = os.path.join(
        file_path, file_name
    )
    if os.path.exists(acc_file):
        with open(acc_file, 'r+') as f:
            acc_data = json.loads(f.readlines()[0])
            # print(json.loads(acc_data))
            if type(args[0]) == dict:
                acc_data = args[0]
            else:
                acc_data[args[0][0]] = args[0][1]
            f.seek(0)
            f.truncate()
            f.write(json.dumps(acc_data))


def add_user(userIfo):
    '''
    添加用户
    :param userIfo:用户信息 example:'name=Harvey,password=123'
    :return:
    '''
    acc_dic = {
        'id': 1000,
        'name': None,
        'password': None,
        'credit': 15000,
        'balance': 15000,
        'enroll_date': None,
        'expire_date': None,
        'pay_day': 30,
        'status': 0,  # 0 = normal, 1 = locked, 2 = disabled
        'manager': False  # 是否是管理员
    }
    acc_dic['enroll_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=3650)
    acc_dic['expire_date'] = (now + delta).strftime('%Y-%m-%d %H:%M:%S')
    file_num = dbrecord.get_file_num()
    acc_dic['id'] = file_num + 1
    print(acc_dic['id'],file_num)
    file_name = '%s.json' % str(acc_dic['id'])
    file_path = db_handle.db_handle(settings.db_info)
    print(file_path, file_name)
    acc_file = os.path.join(
        file_path, file_name
    )
    for item in userIfo.strip().split(','):
        i = item.split('=')
        # for i in item.split('='):
        acc_dic[i[0]] = i[1]
    print(acc_file)
    with open(acc_file, 'w') as f:
        f.write(json.dumps(acc_dic))
        f.flush()
    print(acc_dic)


def modity_limit(acc_id, new_limit):
    '''
    修改额度
    :param acc_id: 用户id
    :param new_limit: 新的额度
    :return:
    '''
    try:
        mod_col = ('credit', new_limit)
        mod_file(acc_id, mod_col)
    except Exception as e:
        print(e)
    else:
        print('账户已修改成功')


def freeze_user(acc_id):
    '''
    冻结用户
    :param acc_id:用户id
    :return:
    '''
    try:
        mod_col = ('status', 1)
        mod_file(acc_id, mod_col)
    except Exception as e:
        print(e)
    else:
        print('账户已冻结')


def mod_balance(acc_id, new_balance):
    try:
        mod_col = ('balance', new_balance)
        mod_file(acc_id, mod_col)
    except Exception as e:
        print(e)
    else:
        print('操作成功')




# add_user('name=Harvey,password=123,manager=True')
