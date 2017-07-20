#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/13
# @Author : trl
from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
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
