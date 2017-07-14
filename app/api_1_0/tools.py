#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from flask import jsonify


def json_response(flag, code, msg, data):
    ret = dict(flag=flag, code=code, msg=msg, data=data)

    return jsonify(ret)
