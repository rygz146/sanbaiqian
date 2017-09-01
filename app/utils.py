#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
app.utils
~~~~~~~~~~~~~~~~~~~~

自定义的一些方法
"""

from flask import jsonify


def json_response(status_code, data, msg='success'):
    ret = dict(status_code=status_code, msg=msg, data=data)

    return jsonify(ret)


def json_page_response(status_code, pagination, data, msg='success'):
    ret = dict(status_code=status_code,
               msg=msg,
               total_num=pagination.pages,
               current_num=pagination.page,
               prev_num=pagination.prev_num,
               next_num=pagination.next_num,
               data=data)

    return jsonify(ret)
