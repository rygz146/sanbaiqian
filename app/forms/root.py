#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
app.forms.root
~~~~~~~~~~~~~~~~~~~~

introduce
"""

from flask_wtf.form import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SchoolForm(FlaskForm):
    name = StringField(label='名称', validators=[DataRequired(message='请输入学校名称')])
    address = StringField(label='详细地址')
    submit = SubmitField(label='添加')