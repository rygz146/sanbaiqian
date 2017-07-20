#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import main
from flask import current_app, render_template
from flask_sqlalchemy import get_debug_queries
from app.log import Logger, slow_query_log
# from ..models.user import User
# from ..emchat.client.emchat_client import get_instance
# from ..emchat.utils.types import service_users

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


# @main.route('/<modify>/emchat_test_users/')
# def create_emchat_test_users(modify):
#     users = User.query.all()
#     service_user = get_instance(service_users)
#     if modify == 'create':
#         for u in users:
#             u_info = {
#                 'username': u.username,
#                 'password': '123456',
#                 'nickname': u.username
#             }
#             test_success, test_result = service_user.create_new_user(payload=u_info)
#             if test_success:
#                 print "registered new user {}".format(u.username)
#             else:
#                 print "failed to register new user {}".format(u.username)
#     elif modify == 'delete':
#         pass
#     else:
#         return '错误的操作'


@main.route('/')
def index():
    # service_user = get_instance(service_users)
    # users = service_user.query_users(limit=10)

    return render_template('main/index.html')
