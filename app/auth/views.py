#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import auth
from ..models.user import User, teacher_permission
from flask_login import login_user, logout_user, login_required
from flask import render_template, current_app, redirect, request, url_for
from flask_principal import identity_changed, Identity, AnonymousIdentity
from ..forms.user import LoginForm


@auth.route('/')
def main():
    users = User.query.all()
    form = LoginForm()
    return render_template(
        'auth.html',
        users=users,
        form=form
    )


@auth.route('/login')
def login():
    u = User.query.get(4)
    login_user(user=u)
    identity_changed.send(
        current_app._get_current_object(),
        identity=Identity(u.id)
    )

    return render_template(
        'login.html'
    )


@auth.route('/logout')
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )

    return redirect(url_for('.main'))
