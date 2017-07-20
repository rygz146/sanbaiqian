#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/13
# @Author : trl
from flask_wtf.form import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    files = FileField(label='图片', validators=[DataRequired(message='请选择图片')])
    submit = SubmitField(label='上传')
