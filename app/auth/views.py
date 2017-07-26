#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/12
# @Author : trl
from . import auth
from ..models.user import db, User, UploadFile, Role
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, current_app, redirect, request, url_for, \
    flash, abort, send_from_directory
from flask_principal import identity_changed, Identity, AnonymousIdentity
from ..forms.user import LoginForm, RegisterForm
from ..forms.upload import UploadForm
from app.log import Logger
from ..upload import files, md5_filename
import os


auth_log = Logger('auth_log', 'auth.log', True)


@auth.route('/')
@login_required
def index():
    roles_table = {'teacher': 'teacher', 'parent': 'parent'}
    for role in current_user.roles:
        roles_table.pop(role.name, '')

    return render_template('auth/index.html',
                           title='用户系统',
                           roles_table=roles_table)


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
            login_user(user=new_user)
            identity_changed.send(
                current_app._get_current_object(),
                identity=Identity(new_user.id)
            )
            return redirect(url_for('auth.index'))
        else:
            flash(message='用户名已被占用', category='warning')

    return render_template('auth/register.html',
                           title='注册',
                           form=form)


@auth.route('/apply/<role_name>', methods=['GET', 'POST'])
@login_required
def apply_role(role_name):
    roles_table = ['teacher', 'parent']
    user_roles = [r.name for r in current_user.roles]
    if role_name in roles_table:
        if role_name in user_roles:
            flash(message='您已经拥有该角色，不能重复申请', category='error')
        else:
            current_user.roles.append(Role.query.filter_by(name=role_name).first())
            db.session.add(current_user)
            db.session.commit()
    else:
        flash(message='该角色不在您的可申请范围，请联系管理员', category='error')

    return redirect(url_for('auth.index'))


@auth.route('/login', methods=['GET', 'POST'])
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
            return form.redirect('auth.index')
        else:
            flash(message='用户名或密码错误', category='error')

    return render_template('auth/login.html',
                           title='登录',
                           form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )

    return redirect(url_for('main.index'))


@auth.route('/files/')
@login_required
def file_system():
    form = UploadForm()
    page = request.args.get('page', 1, int)
    pagination = UploadFile.query.filter_by(user=current_user).paginate(page=page, per_page=5, error_out=False)
    upload_files = pagination.items

    return render_template('auth/file-system.html',
                           title='文件系统',
                           form=form,
                           files=upload_files,
                           pagination=pagination)


@auth.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        upload_files = form.files.raw_data
        for f in upload_files:
            real_name = f.filename
            f.filename = md5_filename(current_user, real_name)
            if UploadFile.has_file(f.filename):
                flash('文件{}已经存在'.format(real_name), category='warning')
            else:
                try:
                    path = files.save(f, folder=current_user.username)
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

    return redirect(url_for('auth.file_system'))


@auth.route('/download/<file_id>/')
@login_required
def download_file(file_id):
    f = UploadFile.query.get_or_404(file_id)
    if f.user == current_user:
        if os.path.isfile(os.path.join(current_app.config['UPLOADED_FILES_DEST'], f.path)):
            return send_from_directory(current_app.config['UPLOADED_FILES_DEST'],
                                       f.path,
                                       attachment_filename=f.name,
                                       as_attachment=True)
        else:
            db.session.delete(f)
            db.session.commit()
            abort(410)
    else:
        abort(403)


@auth.route('/delete/<file_id>/')
@login_required
def delete_file(file_id):
    f = UploadFile.query.get_or_404(file_id)
    file_local_path = os.path.join(current_app.config['UPLOADED_FILES_DEST'], f.path)
    if f.user == current_user:
        if os.path.isfile(file_local_path):
            try:
                db.session.delete(f)
            except:
                db.session.rollback()
            else:
                db.session.commit()
                os.remove(file_local_path)
            return redirect(url_for('auth.file_system'))
        else:
            db.session.delete(f)
            db.session.commit()
            abort(410)
    else:
        abort(403)
