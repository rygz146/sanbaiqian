#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import (
    views,
)
