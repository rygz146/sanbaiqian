#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import db
from sqlalchemy.exc import IntegrityError
from random import seed
import forgery_py


class City(db.Model):
    """
    省市（区）县邮政编码
    """
    __tablename__ = 'city_code'

    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(128), nullable=False)
    province_code = db.Column(db.Integer, nullable=False, index=True)
    city = db.Column(db.String(128), nullable=False)
    city_code = db.Column(db.Integer, unique=True)
    district = db.Column(db.String(128), nullable=False)
    schools = db.relationship('School', backref='city', lazy='dynamic')

    @staticmethod
    def generate_fake(count=10):
        seed()
        for i in range(count):
            c = City(province=forgery_py.address.country(),
                     province_code=forgery_py.address.zip_code(),
                     city=forgery_py.address.city(),
                     city_code=forgery_py.address.zip_code(),
                     district=forgery_py.address.street_name())
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
    create_time = db.Column(db.DateTime(), default=db.func.now())
    city_id = db.Column(db.Integer, db.ForeignKey('city_code.id'))
    users = db.relationship('User', backref='school', lazy='dynamic')
    school_grades = db.relationship('SchoolGrade', backref='school', lazy='dynamic')
    school_classes = db.relationship('SchoolClass', backref='school', lazy='dynamic')

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
    create_time = db.Column(db.DateTime(), default=db.func.now())
    school_classes = db.relationship('SchoolClass', backref='school_grade', lazy='dynamic')

    def __init__(self, **kwargs):
        super(SchoolGrade, self).__init__(**kwargs)

    def __repr__(self):
        return '<SchoolGrade id: {}>'.format(self.id)


teacher_to_class = db.Table(
    'teacher_to_class',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('school_class', db.Integer, db.ForeignKey('school_class.id'))
)


class SchoolClass(db.Model):
    __tablename__ = 'school_class'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school_grade_id = db.Column(db.Integer, db.ForeignKey('school_grade.id'))
    create_time = db.Column(db.DateTime(), default=db.func.now())
    students = db.relationship('Child', backref='school_class', lazy='dynamic')
    class_schedules = db.relationship('ClassSchedule', backref='school_class', lazy='dynamic')

    def __init__(self, **kwargs):
        super(SchoolClass, self).__init__(**kwargs)

    def __repr__(self):
        return '<SchoolClass id: {}>'.format(self.id)


class Child(db.Model):
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Boolean)
    school_class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime(), default=db.func.now())

    def __init__(self, **kwargs):
        super(Child, self).__init__(**kwargs)

    def __repr__(self):
        return '<Child id: {}>'.format(self.id)


class ClassSchedule(db.Model):
    __tablename__ = 'class_schedule'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date(), index=True)
    weekday = db.Column(db.Integer)
    school_class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'))
    class_lessons = db.relationship('ClassLesson', backref='class_schedule', lazy='dynamic')

    def __init__(self, **kwargs):
        super(ClassSchedule, self).__init__(**kwargs)

    def __repr__(self):
        return '<ClassScheduler id: {}>'.format(self.id)


teacher_to_lesson = db.Table(
    'teacher_to_lesson',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('class_lesson_id', db.Integer, db.ForeignKey('class_lesson.id'))
)


lesson_to_file = db.Table(
    'lesson_to_file',
    db.Column('upload_file_id', db.Integer, db.ForeignKey('upload_file.id')),
    db.Column('class_lesson_id', db.Integer, db.ForeignKey('class_lesson.id'))
)


class ClassLesson(db.Model):
    __tablename__ = 'class_lesson'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512))
    content = db.Column(db.Text)
    class_schedule_id = db.Column(db.Integer, db.ForeignKey('class_schedule.id'))
    lesson_files = db.relationship('UploadFile',
                                   secondary=lesson_to_file,
                                   backref=db.backref('teachers', lazy='dynamic'),
                                   lazy='dynamic')

    def __init__(self, **kwargs):
        super(ClassLesson, self).__init__(**kwargs)

    def __repr__(self):
        return '<ClassLesson id: {}>'.format(self.id)
