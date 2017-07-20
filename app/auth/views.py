#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import auth
from ..models.user import db, User, UploadFile
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, current_app, redirect, request, url_for, \
    flash, abort, send_from_directory
from flask_principal import identity_changed, Identity, AnonymousIdentity
from ..forms.user import LoginForm, RegisterForm
from ..forms.upload import UploadForm
from app.log import Logger
from ..upload import files, md5_filename
import os
from urlparse import urlparse, urljoin


auth_log = Logger('auth_log', 'auth.log', True)

# 以下三个方法参考，主要处理登录重定向
# http://flask.pocoo.org/snippets/62/


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    target = request.form.get('next')
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


@auth.route('/')
def index():

    return render_template('auth/index.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None:
            new_user = User(username=form.username.data,
                            password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash(message='注册成功，请登录完善信息', category='success')
            return redirect(url_for('auth.login'))
        else:
            flash(message='用户名已被占用', category='warning')

    return render_template('auth/register.html',
                           form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_url = get_redirect_target()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and u.verify_password(form.password.data):
            login_user(user=u)
            identity_changed.send(
                current_app._get_current_object(),
                identity=Identity(u.id)
            )
            return redirect_back('auth.index')
        else:
            flash(message='用户名或密码错误', category='error')

    return render_template('auth/login.html',
                           next=next_url,
                           form=form)


@auth.route('/logout')
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

    return render_template('auth/information.html',
                           form=form,
                           files=upload_files,
                           pagination=pagination)


@auth.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        upload_files = form.files.raw_data
        for f in upload_files:
            real_name = f.filename
            f.filename = md5_filename(current_user, real_name)
            try:
                if UploadFile.has_file(f.filename):
                    flash('文件{}已经存在'.format(real_name), category='warning')
                else:
                    path = files.save(f, folder=current_user.username, name=real_name)
                    f_stat = os.stat(os.path.join(current_app.config['UPLOADED_FILES_DEST'], path))
                    new_file = UploadFile(path=path,
                                          name=real_name,
                                          size=f_stat.st_size,
                                          user=current_user,
                                          md5_name=f.filename)
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


@auth.route('/show/<file_id>/')
@login_required
def show(file_id):
    f = UploadFile.query.get(file_id)
    if f and os.path.isfile(os.path.join(current_app.config['UPLOADED_FILES_DEST'], f.path)):
        return send_from_directory(current_app.config['UPLOADED_FILES_DEST'], f.path)
    abort(404)
