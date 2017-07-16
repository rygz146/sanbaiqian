#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_principal import Permission, RoleNeed
from sqlalchemy.exc import IntegrityError
from random import seed, choice
import forgery_py
import uuid


ROLES = ['root', 'admin', 'user', 'teacher', 'parent']

root_permission = Permission(RoleNeed('root'))
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))
teacher_permission = Permission(RoleNeed('teacher'))
parent_permission = Permission(RoleNeed('parent'))


class Role(db.Model):
    __tablename__ = 'edu_role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    @staticmethod
    def insert_role():
        for r in ROLES:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r, description=r)
                db.session.add(role)
                db.session.commit()

    def __repr__(self):
        return "<Role {}>".format(self.name)


user_role = db.Table(
    'edu_user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('edu_user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('edu_role.id'))
)


class User(db.Model, UserMixin):
    __tablename__ = 'edu_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    create_time = db.Column(db.DateTime(), default=db.func.now())
    uuid = db.Column(db.String(45), unique=True)
    roles = db.relationship(
        'Role',
        secondary=user_role,
        backref=db.backref('users', lazy='dynamic'),
        lazy='dynamic'
    )

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
        except:
            return None
        else:
            return User.query.get(data['id'])

    @staticmethod
    def generate_fake(count=100):
        seed()
        for i in range(count):
            r = Role.query.get(choice([1, 2, 3, 4, 5]))
            u = User(
                username=forgery_py.internet.user_name(True),
                password='123456'
            )
            u.roles.append(r)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return '<User {}>'.format(self.username)
