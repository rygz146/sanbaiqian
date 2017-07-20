#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl
from app.root import root
from app.models.user import root_permission
from app.log import Logger
from flask import abort, render_template

root_log = Logger('root_log', 'root.log', True)


@root.before_request
def root_before_request():
    if not root_permission.can():
        abort(403)


@root.route('/')
def index():

    return render_template('root/index.html')
