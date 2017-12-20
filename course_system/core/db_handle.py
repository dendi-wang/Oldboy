#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Harvey Wang


def file_db_handle(db_info):
    '''
    获取账户信息文件目录
    :param db_info: db信息
    :return:
    '''
    #db_path = '%s/%s' % (db_info['PATH'], db_info['name'])
    return db_info['PATH']


def mysql_db_handle(db_info):
    pass


def db_handle(db_info):
    '''
    连接db
    :param db_info:db信息
    :return:
    '''
    if db_info['db_engine'] == 'file':
        return file_db_handle(db_info)

    if db_info['db_engine'] == 'mysql':
        return mysql_db_handle(db_info)
