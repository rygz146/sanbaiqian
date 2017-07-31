#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from app import create_app
from app.config import ProductionConfig

app = create_app(ProductionConfig)

if __name__ == '__main__':
    app.run()
