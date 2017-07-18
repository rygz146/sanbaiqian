#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
import sys
from flask_sqlalchemy import SQLAlchemy

reload(sys)
sys.setdefaultencoding('utf-8')

db = SQLAlchemy()

from . import (
    user,
    school
)
