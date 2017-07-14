#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from flask import Flask
from .models import db, user
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u"当前页面需要登录才可访问"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return user.User.query.get(user_id)


toolbar = DebugToolbarExtension()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_name)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
