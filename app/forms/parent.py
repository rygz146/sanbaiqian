#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/31
# @Author : trl
from flask_wtf.form import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired


class ChildForm(FlaskForm):
    name = StringField(label='姓名', validators=[DataRequired(message='请输入孩子姓名')])
    gender = SelectField(label='性别', coerce=bool, choices=[(True, '男'), (False, '女')])
    birthday = DateField(label='出生年月')
    submit = SubmitField(label='添加')
