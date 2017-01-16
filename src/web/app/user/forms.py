# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Xiao Weiwei : Init

from flask_wtf import Form
from wtforms.validators import data_required, length, Email, EqualTo
from .validators import EmailUnique, AccountUnique
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField


class UserCreateForm(Form):
    name = StringField('name', validators=[
        data_required(message='用户名未填'),
        length(1, 64, message='用户名过长'),
        AccountUnique()])
    email = EmailField('Email', validators=[
        data_required(message='邮箱未填'),
        Email(message='无效的邮箱'),
        EmailUnique()])
    password = PasswordField('New Password', validators=[length(5, 64),
                                                         data_required(message='密码未填'),
                                                         EqualTo('confirm', message='两次输入密码必须一致')])
    confirm = PasswordField('Repeat Password', validators=[length(5, 64),
                                                           data_required(message='密码未填')])


class UserEditForm(Form):
    name = StringField('name', validators=[
        data_required(message='用户名未填'),
        length(1, 64, message='用户名过长'),
    ])
    email = EmailField('Email', validators=[
        data_required(message='邮箱未填'),
        Email(message='无效的邮箱'),
    ])
    password = PasswordField('New Password', validators=[length(5, 64),
                                                         data_required(message='密码未填'),
                                                         EqualTo('confirm', message='两次输入密码必须一致')])
    confirm = PasswordField('Repeat Password', validators=[length(5, 64),
                                                           data_required(message='密码未填')])
