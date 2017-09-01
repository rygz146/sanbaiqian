#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
root
~~~~~~~~~~~~~~~~~~~~

关于站点管理员会使用的一些api接口
"""

from flask import request

from . import api
from ..utils import json_page_response
from ..models import db
from ..models.user import User, Role


@api.route('/users')
def get_users():
    page = request.args.get('page', 1, int)
    query_type = request.args.get('query', 'all', str)
    if query_type == 'all':
        pagination = db.session.query(User).paginate(page=page,
                                                     per_page=5,
                                                     error_out=False)
        users = pagination.items
        data = [u.to_json() for u in users]
    else:
        role = Role.query.filter_by(name=query_type).first()
        pagination = db.session.query(User).filter(User.roles.contains(role)).paginate(page=page,
                                                                                       per_page=5,
                                                                                       error_out=False)
        users = pagination.items
        data = [u.to_json() for u in users]

    return json_page_response(200, pagination, data)
