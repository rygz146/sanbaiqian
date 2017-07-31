#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
import os
from flask_uploads import DEFAULTS, AUDIO, ARCHIVES


basedir = os.path.abspath(os.path.dirname(__file__))
EXTEND = tuple('mp4 avi rm rmvb ppt pptx exe'.split())


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.1
    UPLOADED_FILES_DEST = os.path.join(basedir, 'uploads')
    UPLOADED_FILES_ALLOW = DEFAULTS + AUDIO + ARCHIVES + EXTEND


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
