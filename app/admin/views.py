#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl

from flask import abort, render_template

from . import admin
from ..models.user import admin_permission
from ..log import Logger


admin_log = Logger('admin_log', 'admin.log', True)


@admin.before_request
def admin_before_request():
    if not admin_permission.can():
        abort(403)


@admin.route('/')
def index():

    return render_template('admin/index.html')
