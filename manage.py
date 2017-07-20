#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from flask_script import Manager
from app import create_app
from app.config import DevelopmentConfig
from app.models import db, school, user
from flask_migrate import Migrate, MigrateCommand

app = create_app(DevelopmentConfig)

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def init_test_db():
    db.drop_all()
    db.create_all()
    user.Role.insert_role()
    school.City.generate_fake()
    school.School.generate_fake()
    user.User.generate_fake()

if __name__ == '__main__':
    manager.run()
