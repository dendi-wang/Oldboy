#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, UnicodeText, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import or_, and_
from sqlalchemy import func
from sqlalchemy_utils import ChoiceType, PasswordType

Base = declarative_base()


class User_info(Base):
    __tablename__ = 'user_info'
    Type = [
        (1, u'Teacher'),
        (2, u'Student'),
    ]
    Ismanager = [
        (1, u'manager'),
        (0, u'domestic')
    ]
    id = Column(Integer, primary_key=True, autoincrement=True),
    qq = Column(String(11), unique=True)
    username = Column(String(64), nullable=False)
    password = Column(PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecated=['md5_crypt']))
    type = Column(Integer, ChoiceType(Type))
    ismanager = Column(Integer, ChoiceType(Ismanager))

    def __repr__(self):
        return self.username, self.qq


user_m2m_classes = Table('user_m2m_classes', Base.metadata,
                         Column('user_id', Integer, ForeignKey('user_info.id')),
                         Column('classes_id'), Integer, ForeignKey('classes.id')
                         )


class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, autoincrement=True),
    name = Column(String(50), nullable=False)
    outline = Column(String(50), nullable=False)
    price = Column(String(50), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship('Course')
    member = relationship('User_info', secondary=user_m2m_classes, backref='classes')

    def __repr__(self):
        return self.name


class Course_content(Base):
    __tablename__ = 'course_content'
    id = Column(Integer, primary_key=True, autoincrement=True),
    name = Column(String(50), nullable=False, unique=True)
    time = Column(String(50), nullable=False)


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True, autoincrement=True),
    name = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class Classes_record(Base):
    __tablename__ = 'classes_record'
    id = Column(Integer, primary_key=True, autoincrement=True),
    user_id = Column(Integer, ForeignKey('user_info.id'))
    classes_id = Column(Integer, ForeignKey('classes.id'))
    content = Column(Integer, ForeignKey('course_content.id'))


class Homework(Base):
    __tablename__ = 'homework'
    id = Column(Integer, primary_key=True, autoincrement=True),
    student_id = Column(Integer, ForeignKey('user_info.id'))
