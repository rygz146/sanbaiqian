#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl
from . import root
from ..models.user import root_permission
from ..log import Logger
from flask import abort

root_log = Logger('root_log', 'root_log.log', True)


@root.before_request
def root_before_request():
    if not root_permission.can():
        abort(403)


@root.route('/')
def index():
    return 'root'
