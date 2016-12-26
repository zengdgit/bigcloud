# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init


from flask import Flask, request, jsonify, render_template, url_for, redirect
from . import monitor
from flask_login import login_required


@monitor.route('/')
@login_required
def index():
    return redirect(url_for('monitor.info'))


@monitor.route('/info')
@login_required
def info():
    return render_template('monitor/monitor_info.html')

@monitor.route('/channel')
@login_required
def channel():
    return render_template('monitor/monitor_channel.html')

@monitor.route('/log')
@login_required
def log():
    return render_template('monitor/monitor_log.html')
