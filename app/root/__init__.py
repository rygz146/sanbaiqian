#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl
from flask import Blueprint


root = Blueprint('root',
                 __name__,
                 url_prefix='/root')

from . import (views,)
