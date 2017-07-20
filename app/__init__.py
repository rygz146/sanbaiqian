#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from flask import Flask
from .models import db, user
from flask_login import LoginManager, current_user
from flask_debugtoolbar import DebugToolbarExtension
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
from .forms import csrf
from flask_uploads import configure_uploads, patch_request_class
from .upload import files
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u"当前页面需要登录才可访问"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return user.User.query.get(user_id)


toolbar = DebugToolbarExtension()
principal = Principal()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_name)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)
    principal.init_app(app)
    csrf.init_app(app)
    configure_uploads(app, files)
    patch_request_class(app, 128 * 1024 * 1024)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Change the role via add the Need object into Role.

           Need the access the app object.
        """

        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity user object
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity user object
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    @app.errorhandler(404)
    def app_400(request):
        return '{code}: {name}'.format(code=request.code, name=request.name)

    @app.template_filter('gender')
    def gender(gen):
        return '男' if gen else '女'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .teacher import teacher as teacher_blueprint
    app.register_blueprint(teacher_blueprint)

    from .parent import parent as parent_blueprint
    app.register_blueprint(parent_blueprint)

    from .root import root as root_blueprint
    app.register_blueprint(root_blueprint)

    return app
