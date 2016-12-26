# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init


from flask import Flask, request, jsonify, render_template, url_for, redirect
from . import push
from flask_login import login_required


@push.route('/')
@login_required
def index():
    return redirect(url_for('push.littlecloud'))


@push.route('/littlecloud')
@login_required
def littlecloud():
    return render_template('push/push_littlecloud.html')

@push.route('/usergroup')
@login_required
def usergroup():
    return render_template('push/push_usergroup.html')

@push.route('/application')
@login_required
def application():
    return render_template('push/push_application.html')

@push.route('/package')
@login_required
def package():
    return render_template('push/push_package.html')

@push.route('/classification_of_application')
@login_required
def classification_of_application():
    return render_template('push/classification_of_application.html')
