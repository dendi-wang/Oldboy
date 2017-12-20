#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Harvey Wang
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from core import db_handle
from conf import settings
import pickle


class Schoolmember(object):
    def __init__(self, name, age, sex, school_obj, classes_obj=None):
        self.name = name
        self.age = age
        self.sex = sex
        self.school_obj = school_obj
        self.classes_obj = classes_obj

    def regist(self):
        db_file = '%s/stu/%s' % (db_handle.db_handle(settings.db_info), self.name)
        # print(db_file, '=====')
        userInfo = {
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'school_obj': self.school_obj,
            'classes_obj': self.classes_obj
        }
        with open(db_file, 'wb') as f:
            pickle.dump(userInfo, f)


class Teacher(Schoolmember):
    def show_student(self):
        return self.classes_obj.student_list

class Student(Schoolmember):
    def __init__(self, name, age, sex, school_obj, classes_obj=None, pay_status=False):
        super(Student, self).__init__(name, age, sex, school_obj, classes_obj)
        self.pay_status = pay_status

    def get_classes(self):
        return self.school_obj.classes

    def pay(self):
        print('你需要支付%s' % self.classes_obj.course_obj.price)
        self.pay_status = True

    def choice_classes(self, classes_obj):
        self.classes_obj = classes_obj
        self.classes_obj.add_stu(self)
        self.regist()

# S1 = Student('LL', '22', 'M', 'sh')
# S1.regist()
