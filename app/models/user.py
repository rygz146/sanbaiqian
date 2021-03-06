#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl

import forgery_py
import uuid

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          SignatureExpired,
                          BadTimeSignature,
                          BadSignature)
from flask import current_app
from flask_principal import Permission, RoleNeed
from sqlalchemy.exc import IntegrityError
from random import seed, choice
from datetime import datetime
from hashlib import md5

from . import db
from .school import School

# ==================角色定义=======================
ROLES = ['root', 'admin', 'teacher', 'parent']
ROLES_MAP = {
    'root': '站点管理员',
    'admin': '学校管理员',
    'teacher': '教师',
    'parent': '家长'
}
root_permission = Permission(RoleNeed('root'))
admin_permission = Permission(RoleNeed('admin'))
teacher_permission = Permission(RoleNeed('teacher'))
parent_permission = Permission(RoleNeed('parent'))
# ==================权限声明=======================


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


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.Boolean, default=True)
    phone = db.Column(db.String(20), unique=True)
    create_time = db.Column(db.DateTime(), default=datetime.now())
    uniqueID = db.Column(db.String(32), unique=True)
    roles = db.relationship('Role',
                            secondary=users_to_roles,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
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

    def generate_auth_token(self, expiration=7200):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=expiration
        )
        return s.dumps({'id': self.id})

    @staticmethod
    def create_user(username, password, roles=None, name=None, gender=None, phone=None):
        user = User(username=username,
                    password=password,
                    name=name,
                    gender=gender,
                    phone=phone)
        if not isinstance(roles, (tuple, list)):
            raise TypeError('roles must be tuple or list')
        for r in roles:
            if not isinstance(r, Role):
                raise TypeError('roles\'s item must be class <Role>')
            user.roles.append(r)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (SignatureExpired, BadSignature, TypeError):
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
                     school=s,
                     gender=choice([True, False]),
                     create_time=forgery_py.date.date(past=True),
                     phone=forgery_py.address.phone())
            u.roles.append(r)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'roles': [ROLES_MAP.get(r.name) for r in self.roles],
            'name': self.name,
            'gender': '男' if self.gender else '女',
            'school': self.school.to_json() if self.school else None,
            'create_time': self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }

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
    create_time = db.Column(db.DateTime(), default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def has_file(cls, md5_name):
        return cls.query.filter_by(md5_name=md5_name).first()

    @staticmethod
    def md5_filename(user, filename):
        return md5(user.uniqueID + filename).hexdigest().upper() + '.{}'.format(filename.split('.')[-1])

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
    create_time = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, **kwargs):
        super(Child, self).__init__(**kwargs)
        self.age = int(datetime.now().year - self.birthday.year)

    def __repr__(self):
        return '<Child id: {}>'.format(self.id)
