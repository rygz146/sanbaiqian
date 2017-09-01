#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl

from flask import abort, render_template

from . import teacher
from ..models.user import teacher_permission
from ..log import Logger


teacher_log = Logger('teacher_log', 'teacher.log', True)


@teacher.before_request
def teacher_before_request():
    if not teacher_permission.can():
        abort(403)


@teacher.route('/')
def index():

    return render_template('teacher/index.html')
