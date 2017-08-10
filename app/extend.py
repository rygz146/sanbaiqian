#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/25
# @Author : trl

"""
app.extend
~~~~~~~~~~~~~~~~~

插件引入
自定义模板过滤器
自定义状态码页面
"""

from flask import render_template, request
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_principal import Principal
from flask_uploads import UploadSet

from .models import user


files = UploadSet('files')


class MyTemplateFilter(object):
    def __init__(self, app=None):

        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app):

        @app.template_test('current_link')
        def is_current_link(link):
            return link == request.path

        @app.template_filter('gender')
        def gender(gen):
            return '男' if gen else '女'

        @app.template_filter('role')
        def role(r):
            roles = {
                'root': '站点管理员',
                'admin': '学校管理员',
                'teacher': '教师',
                'parent': '家长'
            }
            return roles.get(r)


class MyErrorHandler(object):
    def __init__(self, app=None):

        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app):
        @app.errorhandler(400)
        def app_400(error):
            return render_template('include/error.html',
                                   error=error,
                                   title=error.code), 400

        @app.errorhandler(403)
        def app_403(error):
            print dir(error)
            return render_template('include/error.html',
                                   error=error,
                                   title=error.code), 403

        @app.errorhandler(404)
        def app_404(error):
            return render_template('include/error.html',
                                   error=error,
                                   title=error.code), 404

        @app.errorhandler(410)
        def app_410(error):
            return render_template('include/error.html',
                                   error=error,
                                   title=error.code), 410

        @app.errorhandler(500)
        def app_500(error):
            return render_template('include/error.html',
                                   error=error,
                                   title=error.code), 500


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u"当前页面需要登录才可访问"
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return user.User.query.get(user_id)


toolbar = DebugToolbarExtension()
principal = Principal()
my_template_filter = MyTemplateFilter()
my_error_handler = MyErrorHandler()

