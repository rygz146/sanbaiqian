#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.config import DevelopmentConfig
from app.models import db, school, user

app = create_app(DevelopmentConfig)

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, school=school)


@manager.command
def init_test_db():
    """
    创建测试数据
    :return: 
    """
    db.drop_all()
    db.create_all()
    user.Role.insert_role()
    school.City.generate_fake()
    school.School.generate_fake()
    user.User.generate_fake()
    roles = user.Role.query.filter_by(name='root').all()
    user.User.create_user(username='root',
                          password='123456',
                          roles=roles,
                          name='root',
                          gender=True,
                          phone='')


@manager.command
def init_db():
    """
    创建正式数据
    :return: 
    """
    db.drop_all()
    db.create_all()
    user.Role.insert_role()
    school.City.create_db()
    roles = user.Role.query.filter_by(name='root').all()
    user.User.create_user(username='root',
                          password='123456',
                          roles=roles,
                          name='root',
                          gender=True,
                          phone='')


if __name__ == '__main__':
    manager.run()
