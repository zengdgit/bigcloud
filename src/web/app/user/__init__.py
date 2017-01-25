# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Xiao Weiwei : Init

from flask import Blueprint

user = Blueprint('user', __name__)

from . import views
