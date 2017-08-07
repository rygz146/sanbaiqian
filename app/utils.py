#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
app.utils
~~~~~~~~~~~~~~~~~~~~

something introduce
"""
from flask import jsonify


def json_response(status_code, data, msg='success'):
    ret = dict(status_code=status_code, msg=msg, data=data)

    return jsonify(ret)


def json_page_response(status_code, total_num, prev_num, next_num, data, msg='success',):
    ret = dict(status_code=status_code,
               msg=msg,
               total_num=total_num,
               prev_num=prev_num,
               next_num=next_num,
               data=data)

    return jsonify(ret)
