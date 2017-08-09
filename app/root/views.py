#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/18
# @Author : trl
from flask import abort, render_template, request, redirect, url_for

from app.root import root
from app.models.user import root_permission, User, School, db
from app.log import Logger


root_log = Logger('root_log', 'root.log', True)


@root.before_request
def root_before_request():
    if not root_permission.can():
        abort(403)


@root.route('/')
def index():

    return render_template('root/index.html')


@root.route('/users')
def user_lists():
    page = request.args.get('page', 1, int)
    pagination = User.query.paginate(page=page, per_page=10, error_out=False)
    users = pagination.items

    return render_template('root/user-lists.html',
                           pagination=pagination,
                           users=users)


@root.route('/schools')
def school_lists():
    page = request.args.get('page', 1, int)
    pagination = School.query.paginate(page=page, per_page=5, error_out=False)
    schools = pagination.items

    return render_template('root/school-lists.html',
                           pagination=pagination,
                           schools=schools)


@root.route('/schools/<manage>', methods=['GET', 'POST'])
def school_manage(manage):
    if manage == 'add' and request.method == 'POST':
        form = request.form
        if form.get('name'):
            school = School(name=form.get('name'),
                            address=form.get("address"),
                            city_id=form.get("city_id"))
            db.session.add(school)
            db.session.commit()
    return redirect(url_for('.school_lists'))
