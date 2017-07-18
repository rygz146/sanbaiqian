#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import api
from flask import request, jsonify
from flask_login import login_required, current_user
from app.models.user import User
from app.log import Logger

api_log = Logger('api_log', 'api_log.log', True)


@api.before_request
def api_before_request():
    token = request.headers.get('token')
    if token:
        return 'no token'


@api.route('/auth_token/')
@login_required
def get_auth_token():
    token = current_user.generate_auth_token(3600)
    print User.verify_auth_token(token)

    return jsonify({'token': token})
