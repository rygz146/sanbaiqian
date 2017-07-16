#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/13
# @Author : trl
from flask_wtf import CSRFProtect


csrf = CSRFProtect()

from . import (
    user,
)
