#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl
from . import teacher
from ..models.user import teacher_permission
from ..log import Logger
from flask import abort

teacher_log = Logger('teacher_log', 'teacher_log.log', True)


@teacher.before_request
def teacher_before_request():
    if not teacher_permission.can():
        abort(403)


@teacher.route('/')
def index():
    return 'teacher'
