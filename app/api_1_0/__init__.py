#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from flask import Blueprint

api = Blueprint('api', __name__)

from . import (
    views,
    tools
)
