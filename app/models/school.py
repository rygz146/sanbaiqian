#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl

import forgery_py
import os
import xlrd

from sqlalchemy.exc import IntegrityError
from random import seed
from datetime import datetime

from . import db


class City(db.Model):
    """
    省市（区）县邮政编码
    """
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(128), nullable=False, index=True)
    district = db.Column(db.String(128), nullable=False, index=True)
    county = db.Column(db.String(128), nullable=False)
    zip_code = db.Column(db.String(12), index=True)
    schools = db.relationship('School', backref='city', lazy='dynamic')

    @staticmethod
    def create_db():
        f_path = os.path.join(os.path.abspath(os.path.curdir) + os.sep + 'doc' + os.sep + 'zipcode.xls')
        with xlrd.open_workbook(f_path) as f:
            sheet = f.sheet_by_index(0)
            for i in range(sheet.nrows):
                city = City(province=sheet.row_values(i)[0],
                            district=sheet.row_values(i)[1],
                            county=sheet.row_values(i)[2],
                            zip_code='{:0>6}'.format(int(sheet.row_values(i)[3])))
                db.session.add(city)
                db.session.flush()
        db.session.commit()

    @staticmethod
    def generate_fake(count=10):
        seed()
        for i in range(count):
            c = City(province=forgery_py.address.city(),
                     district=forgery_py.address.city(),
                     county=forgery_py.address.street_name(),
                     zip_code=forgery_py.address.zip_code())
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(City, self).__init__(**kwargs)

    def __repr__(self):
        return '<City id: {}>'.format(self.id)


class School(db.Model):
    __tablename__ = 'school'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256))
    create_time = db.Column(db.DateTime(), default=datetime.now())
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    users = db.relationship('User', backref='school', lazy='dynamic')
    grades = db.relationship('SchoolGrade', backref='school', lazy='dynamic')
    classes = db.relationship('SchoolClass', backref='school', lazy='dynamic')
    students = db.relationship('Child', backref='school', lazy='dynamic')

    def to_json(self):
        return {
            'name': self.name,
            'province': self.city.province,
            'district': self.city.district,
            'county': self.city.county,
            'zip_code': self.city.zip_code,
            'create_time': self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def generate_fake(count=10):
        seed()
        for i in range(count):
            s = School(name=forgery_py.internet.user_name(),
                       create_time=forgery_py.date.date(past=True),
                       address=forgery_py.address.street_address(),
                       city_id=i+1)
            db.session.add(s)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(School, self).__init__(**kwargs)

    def __repr__(self):
        return '<School id: {}>'.format(self.id)


class SchoolGrade(db.Model):
    __tablename__ = 'school_grade'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    create_time = db.Column(db.DateTime(), default=datetime.now())
    classes = db.relationship('SchoolClass', backref='school_grade', lazy='dynamic')

    def __init__(self, **kwargs):
        super(SchoolGrade, self).__init__(**kwargs)

    def __repr__(self):
        return '<SchoolGrade id: {}>'.format(self.id)


classes_to_teachers = db.Table(
    'classes_to_teachers',
    db.Column('school_class_id', db.Integer, db.ForeignKey('school_class.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class SchoolClass(db.Model):
    __tablename__ = 'school_class'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school_grade_id = db.Column(db.Integer, db.ForeignKey('school_grade.id'))
    create_time = db.Column(db.DateTime(), default=datetime.now())
    students = db.relationship('Child', backref='class', lazy='dynamic')
    schedule = db.relationship('ClassSchedule', backref='class', lazy='dynamic')
    teachers = db.relationship('SchoolClass',
                               secondary=classes_to_teachers,
                               backref=db.backref('classes', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, **kwargs):
        super(SchoolClass, self).__init__(**kwargs)

    def __repr__(self):
        return '<SchoolClass id: {}>'.format(self.id)


schedules_to_lessons = db.Table(
    'schedules_to_lessons',
    db.Column('class_schedule_id', db.Integer, db.ForeignKey('class_schedule.id')),
    db.Column('class_lesson_id', db.Integer, db.ForeignKey('class_lesson.id'))
)


class ClassSchedule(db.Model):
    __tablename__ = 'class_schedule'

    id = db.Column(db.Integer, primary_key=True)
    school_class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'))
    schedule_type = db.Column(db.Boolean, default=False)  # False(固定,整个学期都执行)，True(动态添加课程)
    term = db.Column(db.Boolean)  # True(上学期) False(下学期)
    lessons = db.relationship('ClassLesson',
                              secondary=schedules_to_lessons,
                              backref=db.backref('schedules', lazy='dynamic'),
                              lazy='dynamic')

    def __init__(self, **kwargs):
        super(ClassSchedule, self).__init__(**kwargs)

    def __repr__(self):
        return '<ClassScheduler id: {}>'.format(self.id)


lessons_to_teachers = db.Table(
    'lessons_to_teachers',
    db.Column('class_lesson_id', db.Integer, db.ForeignKey('class_lesson.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class ClassLesson(db.Model):
    __tablename__ = 'class_lesson'

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    date = db.Column(db.Date(), index=True)
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
    weekday = db.Column(db.Integer)
    teachers = db.relationship('User',
                               secondary=lessons_to_teachers,
                               backref=db.backref('lessons', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, **kwargs):
        super(ClassLesson, self).__init__(**kwargs)

    def __repr__(self):
        return '<ClassLesson id: {}>'.format(self.id)


lessons_to_files = db.Table(
    'lessons_to_files',
    db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id')),
    db.Column('upload_file_id', db.Integer, db.ForeignKey('upload_file.id'))
)


class Lesson(db.Model):
    __tablename__ = 'lesson'

    id = db.Column(db.Integer, primary_key=True)
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(512))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime(), default=datetime.now())
    files = db.relationship('UploadFile',
                            secondary=lessons_to_files,
                            backref=db.backref('lessons', lazy='dynamic'),
                            lazy='dynamic')
    class_lessons = db.relationship('ClassLesson', backref='lesson', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Lesson, self).__init__(**kwargs)

    def __repr__(self):
        return '<ClassLesson id: {}>'.format(self.id)