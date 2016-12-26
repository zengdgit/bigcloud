# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

from flask import Blueprint

connect = Blueprint('connect', __name__)

from . import views
