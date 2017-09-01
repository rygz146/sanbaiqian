#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl

from flask import Blueprint

api = Blueprint('api',
                __name__,
                url_prefix='/api')

from . import (errors,
               school,
               root)

