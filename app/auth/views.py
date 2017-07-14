#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import auth
from app.models.user import User
from flask_login import login_user, current_user, logout_user
from flask import render_template


@auth.route('/')
def main():
    u = User.query.get(1)
    login_user(user=u)

    return render_template(
        'login.html'
    )


@auth.route('/login')
def login():
    if current_user:
        logout_user()
        print current_user

    return render_template(
        'login.html'
    )
