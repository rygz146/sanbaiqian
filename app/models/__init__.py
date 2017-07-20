#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from . import (user,
               school)
