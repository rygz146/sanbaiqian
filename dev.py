#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl

from app import create_app
from app.config import DevelopmentConfig


app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
