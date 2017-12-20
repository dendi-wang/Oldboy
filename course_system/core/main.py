#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Harvey Wang
import os
import sys
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from core.school import School, Classes, Courses
from core.schoolmember import Student, Teacher
from core.db_handle import db_handle
from conf import settings


# classes1 = Classes('python16期', py, '2017-11-11', None)
# school_sh.open_classes(classes1)

def create_teacher(name, age, sex, school_obj):
    teacher_obj = Teacher(name, age, sex, school_obj)
    teacher_file = '%s/teacher/%s' % (db_handle.db_handle(settings.db_info), name)
    with open(teacher_file, 'wb') as f:
        pickle.dump(teacher_obj, f)
    print('讲师创建成功。。。')
    return teacher_obj


def create_classes(name, course_obj, open_time, teacher_obj):
    classes_obj = Classes(name, course_obj, open_time, teacher_obj)
    classes_file = '%s/classes/%s' % (db_handle.db_handle(settings.db_info), name)
    with open(classes_file, 'wb') as f:
        pickle.dump(classes_obj, f)
    return classes_obj


def create_courses(name, price, outline):
    courses_obj = Courses(name, price, outline)
    courses_file = '%s/courses/%s' % (db_handle(settings.db_info), name)
    with open(courses_file, 'wb') as f:
        pickle.dump(courses_obj, f)
    return courses_obj


school_sh = School('老男孩上海分校', '上海', '上海')
school_bj = School('老男孩北京分校', '北京', '北京')

linux = create_courses('linux', '7000', '6个月')
python = create_courses('python', '7000', '5个月')
go = create_courses('go', '7000', '6个月')
# courses_file = '%s/courses/%s' % (db_handle(settings.db_info), 'linux')
# with open(courses_file, 'rb') as f:
#     linux = pickle.load(f)
school_bj.open_course(linux)
school_bj.open_course(python)
school_sh.open_course(go)

print(school_bj.course_list[0].price)
