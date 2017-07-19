#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/13
# @Author : trl
from flask_wtf.form import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from flask_uploads import DEFAULTS


class UploadForm(FlaskForm):
    files = FileField(
        label='图片',
        validators=[
            DataRequired(message='请选择图片'),
            FileAllowed(upload_set=DEFAULTS, message='不支持该文件类型')
        ]
    )
    submit = SubmitField(label='上传')
