#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl
from . import parent
from ..models.user import parent_permission
from flask import abort, render_template
from ..log import Logger
from ..forms.parent import Child

parent_log = Logger('parent_log', 'parent.log', True)


@parent.before_request
def parent_before_request():
    if not parent_permission.can():
        abort(403)


@parent.route('/')
def index():
    return render_template('parent/index.html')


@parent.route('/<do_type>/child/', methods=['GET', 'POST'])
def manage_child(do_type='manage'):
    form = Child()
    if do_type == 'add' and form.validate_on_submit():
        print form.birthday.data

    return render_template('parent/manage-child.html',
                           form=form)
