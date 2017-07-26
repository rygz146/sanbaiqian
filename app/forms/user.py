#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/13
# @Author : trl
from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo
from flask import redirect, url_for, request
from urlparse import urlparse, urljoin


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    target = request.args.get('next')
    if is_safe_url(target):
        return target
    else:
        return None


class RedirectForm(FlaskForm):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='auth.index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class LoginForm(RedirectForm):
    username = StringField(label='用户名', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField(label='密码', validators=[DataRequired(message='请输入密码')])
    submit = SubmitField(label='登录')


class RegisterForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField(label='密码',
                             validators=[
                                 DataRequired(message='请输入密码'),
                                 Length(min=6, message='密码长度最少6位')
                             ])
    re_password = PasswordField(label='再次输入',
                                validators=[
                                    DataRequired(message='请再次输入密码'),
                                    EqualTo(fieldname='password', message='两次输入不同')
                                ])
    submit = SubmitField(label='注册')
