# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init


from flask import Flask, request, jsonify, render_template


from . import user
from flask_login import login_required
from .forms import UserCreateForm,UserEditForm

from ..models import User

@user.route('/')
@login_required
def index():
    return render_template('user/user.html')

@user.route('/api/user', methods=['GET'])
@login_required
def get_all_user():
    users = User.query.all()
    dic = []
    for i in users:
        item = {
            "id": i.id,
            "name": i.name,
            "email": i.email,
        }
        dic.append(item)
    res = {"result": True, "data": dic}
    return jsonify(res)

@user.route('/api/user', methods=['POST'])
@login_required
def create_user():
    form = UserCreateForm()
    if form.validate_on_submit():
        user1 = User.query.filter(User.name == form.name.data).first()
        if user1 :
            res_massage = u"Failed! The littlecloud with same name or url have already excisted"
            return jsonify({"result": False, "data": None, "message": res_massage})

        new_cloud = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
        )
        new_cloud.save()
    return jsonify({"result": True, "data": None, "message": u"Add new user successfully!"})
    error = form.errors
    return jsonify({"result": False, "data": None, "message": error})

@user.route('/api/user/<int:id>', methods=['DELETE'])
@login_required
def delete_user_by_id(id):
    user = User.query.get(int(id))
    if user:
        user.delete()
        return jsonify({"result": True, "data": None, "message": "Delete the user successfully!"})
    res_message = u"Failed! The user with id %s is not excisted!" % id
    return jsonify({"result": False, "data": None, "message": res_message})

@user.route('/api/user/<int:id>', methods=['PUT'])
@login_required
def update_littlecloud_by_id(id):
    form = UserEditForm()
    if form.validate_on_submit():
        user = User.query.get(int(id))
        if user:
            user.name = form.name.data
            user.email = form.email.data
            user.password = form.password.data
            user.save()
            return jsonify({"result": True, "data": None, "message": u"Edit new user successfully!"})
        res_message = u"Failed! The user with id %s is not excisted!" % id
        return jsonify({"result": False, "data": None, "message": res_message})

    error = form.errors
    return jsonify({"result": False, "data": None, "message": error})


@user.route('/api/user/<int:id>', methods=['GET'])
@login_required
def get_user_by_id(id):
    user = User.query.get(int(id))
    if user:
        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
        }
        return jsonify({"result": True, "data": data, "message": u"Get the user successfully!"})
    res_message = u"Failed! The user with id %s is not excisted!" % id
    return jsonify({"result": False, "data": None, "message": res_message})