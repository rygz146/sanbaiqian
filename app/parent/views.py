#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl

from flask import abort, render_template, request, redirect, url_for
from flask_login import current_user

from . import parent
from ..models import db
from ..models.user import parent_permission, Child
from ..log import Logger
from ..forms.parent import ChildForm


parent_log = Logger('parent_log', 'parent.log', True)


@parent.before_request
def parent_before_request():
    if not parent_permission.can():
        abort(403)


@parent.route('/')
def index():
    return render_template('parent/index.html')


@parent.route('/children/', methods=['GET', 'POST'])
def child_lists():
    form = ChildForm()
    page = request.args.get('page', 1, int)
    pagination = Child.query.filter_by(parent=current_user).paginate(page=page, per_page=5, error_out=False)
    children = pagination.items

    return render_template('parent/manage-child.html',
                           form=form,
                           pagination=pagination,
                           children=children)


@parent.route('/<do_type>/child/', methods=['GET', 'POST'])
def manage_child(do_type='manage'):
    form = ChildForm()
    child_id = request.args.get('id', None, int)
    if do_type == 'add' and form.validate_on_submit():
        child = Child(name=form.name.data,
                      gender=form.gender.data,
                      birthday=form.birthday.data,
                      parent=current_user)
        db.session.add(child)
        db.session.commit()
    if do_type == 'delete' and child_id:
        child = Child.query.get(child_id)
        db.session.delete(child)
        db.session.commit()

    return redirect(url_for('parent.child_lists'))
