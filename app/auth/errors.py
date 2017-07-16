#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/13
# @Author : trl
from . import auth


@auth.errorhandler(400)
def auth_400(request):

    return '{code}: {name}'.format(code=request.code, name=request.name)


@auth.errorhandler(403)
def auth_403(request):

    return '{code}: {name}'.format(code=request.code, name=request.name)


@auth.errorhandler(404)
def auth_404(request):

    return '{code}: {name}'.format(code=request.code, name=request.name)
