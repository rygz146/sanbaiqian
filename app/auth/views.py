#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import auth
from ..models.user import db, User, UploadFile
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, current_app, redirect, request, url_for, flash, abort, send_from_directory
from flask_principal import identity_changed, Identity, AnonymousIdentity
from ..forms.user import LoginForm, RegisterForm
from ..forms.upload import UploadForm
from app.log import Logger
from ..upload import files
from hashlib import md5
import os

auth_log = Logger('auth_log', 'auth.log', True)


@auth.route('/')
def index():
    page = request.args.get('page', 1, int)
    pagination = User.query.paginate(page=page, per_page=10, error_out=False)
    users = pagination.items

    return render_template(
        'auth/index.html',
        pagination=pagination,
        users=users
    )


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None:
            new_user = User(username=form.username,
                            password=form.password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash(message='用户名已被占用', category='warning')

    return render_template(
        'auth/register.html',
        form=form
    )


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and u.verify_password(form.password.data):
            login_user(user=u)
            identity_changed.send(
                current_app._get_current_object(),
                identity=Identity(u.id)
            )
            return redirect(request.args.get('next') or url_for('auth.index'))
        else:
            flash(message='用户名或密码错误', category='error')

    return render_template(
        'auth/login.html',
        form=form
    )


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )

    return redirect(url_for('.login'))


@auth.route('/information/')
@login_required
def information():
    form = UploadForm()
    page = request.args.get('page', 1, int)
    pagination = UploadFile.query.filter_by(user=current_user).paginate(page=page, per_page=5, error_out=False)
    upload_files = pagination.items

    return render_template(
        'auth/information.html',
        form=form,
        files=upload_files,
        pagination=pagination
    )


@auth.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        upload_files = form.files.raw_data
        for f in upload_files:
            real_name = f.filename
            md5_name = md5(f.filename).hexdigest() + '.{}'.format(f.filename.split('.')[1])
            f.filename = md5_name
            try:
                path = files.save(f, folder=current_user.username, name=real_name)
                new_file = UploadFile(path=path,
                                      name=real_name,
                                      size='',
                                      user=current_user,
                                      md5_name=md5_name)
                db.session.add(new_file)
            except:
                db.session.rollback()
                flash('文件{}上传失败'.format(real_name), category='error')
            else:
                db.session.commit()

    return redirect(url_for('.information'))


@auth.route('/download/<file_id>/')
@login_required
def download(file_id):
    f = UploadFile.query.get(file_id)
    if f and os.path.isfile(os.path.join(current_app.config['UPLOADED_FILES_DEST'], f.path)):
        return send_from_directory(current_app.config['UPLOADED_FILES_DEST'], f.path, as_attachment=True)
    abort(404)
