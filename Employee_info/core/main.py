#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
from core.userOperater import select, add, delete, update

choice_run = {
    1: select,
    2: add,
    3: delete,
    4: update,
}


def main():
    print('员工信息查询系统。。。')

    while True:

        print('''1.查询员工信息
2.添加员工信息
3.删除员工信息
4.修改员工信息
5.退出 ''')
        choice = input('>>')
        if choice == 'q' or choice == '5':
            exit('退出系统')
        if int(choice.strip()) in choice_run:
            flag = True
            while flag:
                sql = input('请输入sql 或返回(b) >>')
                if sql != 'b':
                    ret = choice_run[int(choice)](sql)
                    if ret:
                        pass
                    else:
                        exit('有错误')
                else:
                    flag = False
                    continue
        else:
            print('没有此项选择。。。请重新选择。。。')
