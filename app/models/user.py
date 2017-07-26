#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          SignatureExpired,
                          BadTimeSignature)
from flask import current_app
from flask_principal import Permission, RoleNeed
from sqlalchemy.exc import IntegrityError
from random import seed, choice
import forgery_py
import uuid
from school import School
from datetime import datetime


ROLES = ['root', 'admin', 'teacher', 'parent']

root_permission = Permission(RoleNeed('root'))
admin_permission = Permission(RoleNeed('admin'))
teacher_permission = Permission(RoleNeed('teacher'))
parent_permission = Permission(RoleNeed('parent'))


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(255))

    @staticmethod
    def insert_role():
        db.session.add_all(map(lambda r: Role(name=r, description=r), ROLES))
        db.session.commit()

    def __repr__(self):
        return "<Role id: {}>".format(self.id)


users_to_roles = db.Table(
    'users_to_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


users_schools = db.Table(
    'users_to_schools',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('school_id', db.Integer, db.ForeignKey('school.id'))
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.Boolean, default=True)
    phone = db.Column(db.String(20), unique=True)
    create_time = db.Column(db.DateTime(), default=db.func.now())
    uniqueID = db.Column(db.String(32), unique=True)
    roles = db.relationship('Role',
                            secondary=users_to_roles,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')
    schools = db.relationship('School',
                              secondary=users_schools,
                              backref=db.backref('users', lazy='dynamic'),
                              lazy='dynamic')
    files = db.relationship('UploadFile', backref='user', lazy='dynamic')
    children = db.relationship('Child', backref='parent', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=expiration
        )
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadTimeSignature:
            return None
        else:
            return User.query.get(data['id'])

    @staticmethod
    def generate_fake(count=10):
        seed()
        for i in range(count):
            r = Role.query.get(choice([1, 2, 3, 4]))
            s = School.query.get(choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
            u = User(username=forgery_py.internet.user_name(True),
                     password='123456',
                     name=forgery_py.internet.user_name(),
                     gender=choice([True, False]),
                     create_time=forgery_py.date.date(past=True),
                     phone=forgery_py.address.phone())
            u.schools.append(s)
            u.roles.append(r)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.uniqueID = uuid.uuid4().hex

    def __repr__(self):
        return '<User id: {}>'.format(self.id)


class UploadFile(db.Model):
    __tablename__ = 'upload_file'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    size = db.Column(db.Integer)
    md5_name = db.Column(db.String(32), nullable=False)
    create_time = db.Column(db.DateTime(), default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def has_file(cls, md5_name):
        return cls.query.filter_by(md5_name=md5_name).first()

    def __init__(self, **kwargs):
        super(UploadFile, self).__init__(**kwargs)

    def __repr__(self):
        return '<UploadFile id: {}>'.format(self.id)


class Child(db.Model):
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Boolean)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school_class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    birthday = db.Column(db.Date())
    create_time = db.Column(db.DateTime(), default=db.func.now())

    def __init__(self, **kwargs):
        super(Child, self).__init__(**kwargs)
        self.age = int(datetime.now().year - self.birthday.year)

    def __repr__(self):
        return '<Child id: {}>'.format(self.id)
