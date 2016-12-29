# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init


from flask import Flask, request, jsonify, render_template
from . import connect
from ..models import LittleCloud
from flask_login import login_required


@connect.route('/', methods=['GET'])
@login_required
def index():
    return render_template('connect/connect.html')


@connect.route('/api/littlecloud', methods=['GET'])
@login_required
def get_all_littleclouds():
    # littleclouds = LittleCloud
    return render_template('connect/connect.html')


@connect.route('/api/littlecloud/', methods=['POST'])
@login_required
def add_littlecloud():
    return render_template('connect/connect.html')


@connect.route('/api/littlecloud/<int:id>', methods=['DELETE'])
@login_required
def delete_littlecloud_by_id(id):
    return render_template('connect/connect.html')


@connect.route('/api/littlecloud/<int:id>', methods=['PUT'])
@login_required
def update_littlecloud_by_id(id):
    return render_template('connect/connect.html')


@connect.route('/api/littlecloud/<int:id>', methods=['GET'])
@login_required
def get_littlecloud_by_id(id):
    return render_template('connect/connect.html')
