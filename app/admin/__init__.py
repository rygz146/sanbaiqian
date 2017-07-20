#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl
from flask import Blueprint

admin = Blueprint('admin',
                  __name__,
                  url_prefix='/admin')

from . import (views,)

