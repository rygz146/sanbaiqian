#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/13
# @Author : trl
from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(label='username', validators=[DataRequired()])
    password = PasswordField(label='password', validators=[DataRequired()])
    submit = SubmitField(label='Login')
