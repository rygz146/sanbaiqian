#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import db
from sqlalchemy.exc import IntegrityError
from random import seed
import forgery_py


class City(db.Model):
    __tablename__ = 'edu_city_code'

    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(16), nullable=False)
    province_id = db.Column(db.Integer, unique=True)
    city = db.Column(db.String(16), nullable=False)
    city_id = db.Column(db.Integer, unique=True)
    district = db.Column(db.String(16), nullable=False)
    schools = db.relationship('School', backref='city', lazy='dynamic')

    @staticmethod
    def generate_fake(count=10):
        seed()
        for i in range(count):
            c = City(province=forgery_py.address.country(),
                     province_id=forgery_py.address.zip_code(),
                     city=forgery_py.address.city(),
                     city_id=forgery_py.address.zip_code(),
                     district=forgery_py.address.street_name())
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<City {}>'.format(self.city_id)


class School(db.Model):
    __tablename__ = 'edu_school'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    create_time = db.Column(db.DateTime(), default=db.func.now())
    city_id = db.Column(db.Integer, db.ForeignKey('edu_city_code.id'))

    @staticmethod
    def generate_fake(count=10):
        seed()
        for i in range(count):
            s = School(name=forgery_py.internet.user_name(),
                       create_time=forgery_py.date.date(),
                       city_id=i+1)
            db.session.add(s)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<School {}>'.format(self.name)
