#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl

from flask import Blueprint


parent = Blueprint('parent',
                   __name__,
                   url_prefix='/parent')

from . import (views,)
