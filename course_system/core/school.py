#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Harvey Wang

from core import db_handle
from conf import settings
import pickle

class School(object):
    def __init__(self, name, city, address):
        self.name = name
        self.city = city
        self.address = address
        self.classes = []
        self.teacher_list = []
        self.course_list = []

    def open_classes(self, classes_obj):
        self.classes.append(classes_obj)

    def open_course(self, course_obj):
        self.course_list.append(course_obj)

    def add_teacher(self, teacher_obj):
        self.teacher_list.append(teacher_obj)


class Classes(object):
    def __init__(self, name, course_obj, open_time, teacher_obj):
        self.name = name
        self.course_obj = course_obj
        self.open_date = open_time
        self.teacher_obj = teacher_obj
        self.student_list = []

    def add_stu(self, stu_obj):
        self.student_list.append(stu_obj)
        db_classes = '%s/classes/%s' % (db_handle.db_handle(settings.db_info), self.name)
        with open(db_classes, 'ab') as f:
            pickle.dump(self.student_list, f)

class Courses(object):
    def __init__(self, name, price, outline):
        self.name = name
        self.price = price
        self.outline = outline
