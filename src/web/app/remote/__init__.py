# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/02/20 Chen Weijian : Init

from flask import Blueprint

remote = Blueprint('remote', __name__)

from . import views
