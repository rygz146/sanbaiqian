#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
api.errors
~~~~~~~~~~~~~~~~~~~~

接口返回数据异常及错误
"""

from . import api
from ..utils import json_response


@api.errorhandler(400)
def api_400(error):

    return json_response(400, None, error.description)


@api.errorhandler(403)
def api_403(error):

    return json_response(403, None, error.description)


@api.errorhandler(404)
def api_404(error):

    return json_response(404, None, error.description)


@api.errorhandler(500)
def api_500(error):

    return json_response(500, None, error.description)
