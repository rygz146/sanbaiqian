#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl
from app.root import root
from app.models.user import root_permission, User
from app.log import Logger
from flask import abort, render_template, request

root_log = Logger('root_log', 'root.log', True)


@root.before_request
def root_before_request():
    if not root_permission.can():
        abort(403)


@root.route('/')
def index():
    page = request.args.get('page', 1, int)
    pagination = User.query.paginate(page=page, per_page=10, error_out=False)
    users = pagination.items

    return render_template('root/index.html',
                           pagination=pagination,
                           users=users)
