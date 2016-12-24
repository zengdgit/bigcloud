# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

import json
import time
from flask import Flask, request, jsonify, render_template, url_for, redirect
from . import auth
from ..models import User
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm


@auth.route('/')
def index():
    return 'hello world flask'


@auth.route('/add/<name>/<password>')
def add(name, password):
    u = User(name=name)
    u.password = password
    try:
        u.save()
    except Exception as e:
        return 'wrong'
    return 'Add %s user successfully' % name


@auth.route('/get/<name>')
def get(name):
    try:
        u = User.query.filter(User.name == name).first()
    except Exception as e:
        return 'there is not %s' % name
    return 'hello %s %s' % (u.name, u.email)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("form is validated.")

        user = User.query.filter(User.name == form.username.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('home.index'))
        # TODO 最好能在页面能提示用户密码不正确
    return render_template('auth/login.html', year=time.strftime('%Y', time.localtime(time.time())), form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    # return render_template('auth/login.html', year=time.strftime('%Y', time.localtime(time.time())))
    return redirect(url_for('auth.login'))
