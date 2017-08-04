#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from flask import current_app, render_template, abort, request, g
from flask_sqlalchemy import get_debug_queries

from app.log import Logger, slow_query_log

from . import main
from ..models.school import School

main_log = Logger('main_log', 'main.log', True)


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            slow_log = 'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' \
                % (query.statement, query.parameters, query.duration, query.context)
            current_app.logger.warning(slow_log)
            slow_query_log.warning(slow_log)
    return response


@main.route('/shutdown')
def app_shutdown():
    if not current_app.testing:
        abort(404)

    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)

        shutdown()
    return '正在关闭服务端进程...'


@main.route('/')
def index():

    return render_template('main/index.html',
                           title='首页')


@main.route('/schools', methods=['GET', 'POST'])
def school_lists():
    page = request.args.get('page', 1, int)
    pagination = School.query.paginate(page=page, per_page=5, error_out=False)
    schools = pagination.items

    return render_template('main/school-lists.html',
                           pagination=pagination,
                           schools=schools)
