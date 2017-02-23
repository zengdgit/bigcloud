# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/02/20 Chen Weijian : Init

from flask import jsonify, render_template, request
from flask_login import login_required, current_user
from . import remote
from .task import TaskBroker
from .. import logger


@remote.route('/connect', methods=['POST'])
def connect():
    '''
    【API】连接大云。
    :return:
    '''
    result = TaskBroker.dispatch(request)
    return jsonify(result)
