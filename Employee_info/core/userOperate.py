#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
from db import dbHelper
import time

db_file, table_field = dbHelper.dbHeler()

def select(sql):
    '''
    :param sql: select * from staff_table where dept like "T"
    :return: result is string
    '''
    sql_info = sql.split(' ')
    sql_field = sql_info[1].split(',')
    if 'where' in sql_info:
        select_require_list = sql_info[-3:]
        # select_require = select_require_list[1] + select_require_list[2]

    ret = []
    with open(db_file, 'r') as f:
        for line in f:
            tmp_ret = line.strip().split(',')
            if len(select_require_list) > 0:
                if select_require_list[1] == '>':
                    if int(tmp_ret[table_field[select_require_list[0]]]) > int(select_require_list[2]):
                        if sql_field[0] == '*':
                            ret.append(line)
                        else:
                            L = []
                            for i in sql_field:
                                L.append(tmp_ret[table_field[i]])
                            ret.append(','.join(L))
                elif select_require_list[1] == '=':
                    if tmp_ret[table_field[select_require_list[0]]].isdigit():
                        tmp_ret[table_field[select_require_list[0]]] = int(tmp_ret[table_field[select_require_list[0]]])
                        select_require_list[2] = int(select_require_list[2])
                    else:
                        select_require_list[2] = select_require_list[2].strip("\'").strip("\"")
                    if tmp_ret[table_field[select_require_list[0]]] == select_require_list[2]:
                        if sql_field[0] == '*':
                            ret.append(line)
                        else:
                            L = []
                            for i in sql_field:
                                L.append(tmp_ret[table_field[i]])
                            ret.append(','.join(L))
                elif select_require_list[1] == 'like':
                    if select_require_list[2].strip("\'").strip("\"") in tmp_ret[table_field[select_require_list[0]]]:
                        if sql_field[0] == '*':
                            ret.append(line)
                        else:
                            L = []
                            for i in sql_field:
                                L.append(tmp_ret[table_field[i]])
                            ret.append(','.join(L))
    return ''.join(ret)


def add(sql):
    '''
     :param sql: 'name=Harvey Wang, age=18, phone=13022222222, dept=python' 只能是这样的形式
     :return: Ture:添加成功
    '''
    sql_info = sql.strip('\'').strip('\"').split(',')
    print(sql_info)
    add_info = {
        'id': None,
        'name': None,
        'age': None,
        'phone': None,
        'dept': None,
        'enroll_date': None
    }
    for item in sql_info:
        add_info[item.split('=')[0].strip()] = item.split('=')[1]
    with open(db_file, 'a+') as f:
        end = f.tell()
        f.seek(0)
        last_line = f.readlines()[-1]
        last_id = int(last_line.split(',')[0])
        new_id = last_id + 1
        add_info['id'] = new_id
        add_info['enroll_date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        add_info = '''
{id},{name},{age},{phone},{dept},{enroll_date}'''.format(**add_info)
        f.seek(end)
        f.write(add_info)
        return True


def update(sql):
    pass


def delete(sql):
    pass

#
# ret = select(sql)
# print(ret)

select('select  * from staff_table where dept = "IT"')
# sql = 'name=Harvey Wang, age=18, phone=13022222222, dept=python'

# add(sql)


# INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)
# insert into staff_table (name,age,phone,dept) values (Harvey Wang,18,13022222222,python)
# UPDATE staff_table SET dept = Market where dept = IT
