#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import main
from flask import render_template, current_app
from flask_sqlalchemy import get_debug_queries
from app.log import Logger, slow_query_log


main_log = Logger('main_log', 'main_log.log', True)


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
def index():

    return render_template(
        'main/index.html'
    )
