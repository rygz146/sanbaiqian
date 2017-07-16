#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import main
from app.models import db
from app.models.user import User, Role
from app.models.school import School, City
from flask import render_template, current_app
from flask_sqlalchemy import get_debug_queries
from app.log import Logger, slow_query_log


app_main_log = Logger('app_main_log', 'app_main_log', True)


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            slow_log = 'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' \
                % (query.statement, query.parameters, query.duration, query.context)
            current_app.logger.warning(slow_log)
            slow_query_log.warning(slow_log)
    return response


@main.route('/')
def main():
    users = db.session.query(User).all()
    schools = School.query.all()
    cities = City.query.all()
    roles = Role.query.all()

    return render_template(
        'test.html',
        users=users,
        schools=schools,
        cities=cities,
        roles=roles
    )
