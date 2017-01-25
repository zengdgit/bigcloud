# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

import time
from flask import request, render_template, url_for, redirect
from . import auth
from ..models import User
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm


@auth.route('/', methods=['GET'])
def index():
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
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
    return redirect(url_for('auth.login'))
