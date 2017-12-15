#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
from db import dbHelper
import os
import time

db_file, table_field = dbHelper.dbHeler()


def not_empty(s):
    return s and s.strip()


def sql_handle(db_engine='file'):
    def outwapper(func):
        def wapper(sql):
            term = sql.strip().split('where')
            term_K = None
            term_p = None
            term_V = None
            if len(term) == 2:
                term_K = list(filter(not_empty, term[1].strip().split(' ')))[0].strip()
                term_p = list(filter(not_empty, term[1].strip().split(' ')))[1].strip()
                term_V = list(filter(not_empty, term[1].strip().split(' ')))[2].strip('\"').strip('\'')
            sql_L = list(filter(not_empty, sql.strip().split(' ')))
            if sql_L[0] == 'select':
                field_L = sql.strip().split('from')[0].strip()
                field = list(filter(not_empty, field_L.split(' ')))[1]
                return func(field, term_K, term_p, term_V)
            elif sql_L[0] == 'update':
                field_L = term[0].strip().split('set')[1].strip()
                field = field_L.split('=')[0]
                value = field_L.split('=')[1].strip('\"').strip('\'')
                return func(field, value, term_K, term_p, term_V)
            elif sql_L[0] == 'insert':
                field_L = list(filter(not_empty, sql.strip().split('values')[0].strip().split(' ')))[-1].strip(
                    '(').strip(')')
                value_L = sql.strip().split('values')[1].strip(' ').strip('(').strip(')')
                return func(field_L, value_L)
            elif sql.isdigit():
                return func(sql)
            else:
                print('语法错误')
                return False

        return wapper

    return outwapper


@sql_handle(db_engine='file')
def select(*sql):
    '''
    sql:'insert into staff_table (name,age,phone,dept) values (Harvey Wang,18,13022223222,python)'
    :return: Ture
    '''
    ret = []
    with open(db_file, 'r') as f:
        for line in f:
            tmp_ret = line.strip().split(',')
            if sql[2] == '>':
                if int(tmp_ret[table_field[sql[1]]]) > int(sql[3]):
                    if sql[0].strip(' ') == '*':
                        ret.append(line)
                    else:
                        L = []
                        for i in sql[0].split(','):
                            L.append(tmp_ret[table_field[i]])
                        ret.append(','.join(L))
            elif sql[2] == '=':
                if tmp_ret[table_field[sql[1]]] == sql[3]:

                    if sql[0] == '*':
                        ret.append(line)
                    else:
                        L = []
                        for iF in sql[0].split(','):
                            L.append(tmp_ret[table_field[i]])
                        ret.append(','.join(L))
            elif sql[2] == '<':
                if int(tmp_ret[table_field[sql[1]]]) < int(sql[3]):
                    if sql[0] == '*':
                        ret.append(line)
                    else:
                        L = []
                        for i in sql[0].split(','):
                            L.append(tmp_ret[table_field[i]])
                        ret.append(','.join(L))
            elif sql[2] == 'like':
                if sql[3] in tmp_ret[table_field[sql[1]]]:
                    if sql[0] == '*':
                        ret.append(line)
                    else:
                        L = []
                        for i in sql[0].split(','):
                            L.append(tmp_ret[table_field[i]])
                        ret.append(','.join(L))
            elif sql[2] == None:
                if sql[0] == '*':
                        ret.append(line)
                else:
                    L = []
                    for i in sql[0].split(','):
                        L.append(tmp_ret[table_field[i]])
                        ret.append(','.join(L))
            else:
                print('语法错误')
    print('\n'.join(ret))
    return True


@sql_handle(db_engine='file')
def add(*sql):
    '''
    :param
    sql:'insert into staff_table (name,age,phone,dept) values (Harvey Wang,18,13022223222,python)'
    :return: Ture:添加成功
    '''
    sql_info_r = sql[0].split(',')
    sql_info_l = sql[1].split(',')
    # print(sql_info_r)
    add_info = {
        'id': None,
        'name': None,
        'age': None,
        'phone': None,
        'dept': None,
        'enroll_date': None
    }
    for i in range(len(sql_info_r)):
        add_info[sql_info_r[i].strip(' ')] = sql_info_l[i]

    with open(db_file, 'a+') as f:
        end = f.tell()
        f.seek(0)
        for line in f:
            line_L = line.split(',')
            # print(add_info['phone'])
            if line_L[3] == add_info['phone'] or add_info['phone'] == None:
                print('phone重复或为空')
                return False
        f.seek(0)
        last_line = f.readlines()[-1]
        last_id = int(last_line.split(',')[0])
        new_id = last_id + 1
        add_info['id'] = new_id
        add_info['enroll_date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        add_line = '''
{id},{name},{age},{phone},{dept},{enroll_date}'''.format(**add_info)
        f.seek(end)
        f.write(add_line)
        print('添加成功')
        return True


@sql_handle(db_engine='file')
def update(*sql):
    '''
    sql:sql = 'update staff_table set dept="Market" where dept = "IT"'
    :return: Ture:修改成功
    '''
    new_file = os.path.join(os.path.dirname(db_file), 'new_file.txt')

    with open(db_file, 'r') as f, open(new_file, 'w') as f_new:
        for line in f:
            tmp_ret = line.strip().split(',')
            if tmp_ret[table_field[sql[2]]] == sql[4]:
                tmp_ret[table_field[sql[2]]] = sql[1]
                f_new.write(','.join(tmp_ret))
                f_new.write('\n')
                f_new.flush()
            else:
                f_new.write(line)
                f_new.flush()
    # t = time.time()
    os.remove(db_file)
    os.rename(new_file, db_file)
    print('修改成功')
    return True


def delete(sql):
    new_file = os.path.join(os.path.dirname(db_file), 'new_file.txt')
    with open(db_file, 'r') as f, open(new_file, 'w') as f_new:
        for line in f:
            tmp_ret = line.strip().split(',')
            if int(tmp_ret[0]) == int(sql):
                continue
            else:
                f_new.write(line)
                f_new.flush()
    # t = time.time()
    # bakfile = '%s_bak' % db_file
    # os.rename(db_file, bakfile)
    os.remove(db_file)
    os.rename(new_file, db_file)
    print('删除成功')
    return True


    #
    # sql = 'select * from staff_table where dept like "T"'
    # ret = select(sql)
    #
    # sql5 = 'insert into staff_table (name,age,phone,dept) values (Harvey Wang,18,13022223222,python)'
    # # sql = 'update staff_table set dept="Market" where dept = "IT"'
    # #add(sql5)
    # # print(update(sql))
    # delete(1)
    # select('select name,age from staff_table where age > 22')
    #
