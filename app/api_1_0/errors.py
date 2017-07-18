#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/13
# @Author : trl
from . import api


@api.errorhandler(400)
def api_400(request):

    return '{code}: {name}'.format(code=request.code, name=request.name)


@api.errorhandler(403)
def api_403(request):

    return '{code}: {name}'.format(code=request.code, name=request.name)


@api.errorhandler(404)
def api_404(request):

    return '{code}: {name}'.format(code=request.code, name=request.name)


@api.errorhandler(500)
def api_500(request):

    return '{code}: {name}'.format(code=request.code, name=request.name)