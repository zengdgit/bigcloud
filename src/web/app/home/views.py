# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init


from flask import Flask, request, jsonify, render_template
from . import home
from flask_login import login_required


@home.route('/')
@login_required
def index():
    return render_template('index.html')
