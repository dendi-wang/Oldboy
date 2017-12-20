#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Harvey Wang

import pickle, os
from core.school import School, Classes, Courses
from core.schoolmember import Student, Teacher
from core.db_handle import db_handle
from conf import settings
from core.main import create_teacher, create_classes, create_courses

school_sh = School('老男孩上海分校', '上海', '上海')
school_bj = School('老男孩北京分校', '北京', '北京')


def manager_view():
    print('''
    创建讲师
    创建课程
    创建班级
    ''')
    choice = input('>>>')
    if choice == '创建讲师':
        name = input('name:')
        age = input('age:')
        sex = input('sex:')
        school = input('school:')
        if school == '上海':
            school_obj = school_sh
        else:
            school_obj = school_bj
        create_teacher(name, age, sex, school_obj)
    elif choice == '创建课程':
        name = input('课程名称:')
        price = input('价格:')
        outline = input('周期:')
        create_courses(name, price, outline)
    elif choice == '创建班级':
        pass


def s_view(school_obj):
    print('''
    注册
    登录
    ''')
    choice = input('请选择操作:')
    if choice == '注册':
        name = input('姓名：')
        age = input('年龄：')
        sex = input('性别：')
        stu = Student(name, age, sex, school_obj, False)
        stu.regist()
        # db_file = '%s/%s' % (db_handle(settings.db_info), name)
        #
        # with open(db_file, 'wb') as f:
        #     f.write(pickle.dumps(stu))
    if choice == '登录':
        name = input('用户名:')
        userFile = '%s/stu/%s' % (db_handle(settings.db_info), name)
        with open(userFile, 'rb') as f:
            stuInfo = pickle.loads(f.read())
            print(stuInfo['classes_obj'].name)
            stu_obj = Student(stuInfo['name'], stuInfo['age'], stuInfo['sex'], stuInfo['school_obj'],
                              stuInfo['classes_obj'])
        while os.path.isfile(userFile):
            print('''
            交学费
            选择班级
            ''')
            choice = input('请输入你的选择:')
            if choice == '选择班级':
                for classes_obj in school_obj.classes:
                    print(classes_obj.name)
                choice_c = input('>>>')
                for classes_obj in school_obj.classes:
                    if choice_c == classes_obj.name:
                        # print(classes_obj)
                        stu_obj.choice_classes(classes_obj)
            elif choice == '交学费':
                stu_obj.pay()
            elif choice == 'q':
                exit()
            else:
                print('No chioce....')
        else:
            exit('用户未注册')


def t_view(teacher_obj):
    print('''
    查看班级学员
    修改成绩
    ''')
    choice = input('>>>')
    if choice == '查看班级学员':
        teacher_obj.show_student()
    elif choice == '修改成绩':
        teacher_obj.mod()
