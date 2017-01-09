# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init


from flask import Flask, request, jsonify, render_template, url_for, redirect
from . import push
from ..models import Package
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


#################
# package
#################
@push.route('/api/package', methods=['GET'])
@login_required
def get_all_packages():
    '''
    【API】得到所有安装包的数据。
    :return: 安装包 ID
    '''
    packages = Package.query.all()
    dic = []
    for i in packages:
        item = {
            "id": i.id,
            "filename": i.filename,
            "relative_path": i.relative_path,
            "identifier": i.identifier,
            "total_size": i.total_size,
            "total_chunks": i.total_chunks,
            "is_complete": i.is_complete,
            "md5": i.md5,
        }
        dic.append(item)
    res = {"result": True, "data": dic, "message": u"Get all packages successfully!"}
    return jsonify(res)


@push.route('/api/package', methods=['POST'])
@login_required
def upload_package():
    '''
    【API】处理上传文件chunk。
    '''
    res = {"result": True, "data": None, "message": u"upload package successfully!"}


@push.route('/api/package/<int:id>', methods=['DELETE'])
@login_required
def delete_package_by_id(id):
    '''
    【API】根据 id 删除安装包。
    :param id: 安装包 ID
    :return:
    '''
    package = Package.query.get(int(id))
    if package:
        package.delete()
        return jsonify({"result": True, "data": None, "message": "Delete the package successfully!"})
    res_message = u"Failed! The package with id %s is not excisted!" % id
    return jsonify({"result": False, "data": None, "message": res_message})
