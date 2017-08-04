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


def json_page_response(status_code, pages, has_prev, prev_num, has_next, next_num, data, msg='success',):
    ret = dict(status_code=status_code,
               msg=msg,
               pages=pages,
               has_prev=has_prev,
               prev_num=prev_num,
               has_next=has_next,
               next_num=next_num,
               data=data)

    return jsonify(ret)
