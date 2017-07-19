#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl
from . import parent
from ..models.user import parent_permission
from flask import abort
from ..log import Logger

parent_log = Logger('parent_log', 'parent.log', True)


@parent.before_request
def parent_before_request():
    if not parent_permission.can():
        abort(403)


@parent.route('/')
def index():
    return 'parent'
