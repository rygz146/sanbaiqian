#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import auth
from ..models.user import User
from flask_login import login_user, logout_user, login_required
from flask import render_template, current_app, redirect, request, url_for
from flask_principal import identity_changed, Identity, AnonymousIdentity
from ..forms.user import LoginForm, RegisterForm
from app.log import Logger

auth_log = Logger('auth_log', 'auth_log.log', True)


@auth.route('/')
def index():
    page = request.args.get('page', 1, int)
    pagination = User.query.paginate(page=page, per_page=10, error_out=False)
    users = pagination.items

    return render_template(
        'auth/index.html',
        pagination=pagination,
        users=users
    )


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    return render_template(
        'auth/register.html',
        form=form
    )


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.get(4)
        login_user(user=u)
        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(u.id)
        )
        return redirect(request.args.get('next') or url_for('auth.index'))

    return render_template(
        'auth/login.html',
        form=form
    )


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )

    return redirect(url_for('.login'))


@auth.route('/information/')
@login_required
def information():

    return render_template(
        'auth/information.html'
    )
