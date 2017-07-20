#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl
from flask import Blueprint


teacher = Blueprint('teacher',
                    __name__,
                    url_prefix='/teacher')

from . import (views,)
