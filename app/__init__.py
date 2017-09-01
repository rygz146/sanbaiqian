#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl

import sys

from flask import Flask, g
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_uploads import configure_uploads, patch_request_class

from .forms import csrf
from .models import db
from .extend import (login_manager,
                     toolbar,
                     files,
                     principal,
                     my_template_filter,
                     my_error_handler)

reload(sys)
sys.setdefaultencoding('utf-8')


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
    my_template_filter.init_app(app)
    my_error_handler.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Change the role via add the Need object into Role.

           Need the access the app object.
        """

        # Set the identity user object
        identity.user = current_user

        # Add current_user to global user
        g.user = current_user

        # Add the UserNeed to the identity user object
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity user object
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

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
