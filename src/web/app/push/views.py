# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

import os
from flask import Flask, request, jsonify, render_template, url_for, redirect
from . import push
from ..models import Package
from ..utils import checksum
from flask_login import login_required, current_user
from .forms import UploadForm
from .. import upload, logger


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
    :return:
    '''
    packages = Package.query.all()
    dic = []
    for i in packages:
        item = {
            "id": i.id,
            "filename": i.filename,
            "url": upload.url(i.filename),
            "size": i.size,
            "md5": i.md5,
        }
        dic.append(item)
    logger.info("{0} - Get all packages".format(current_user.name))
    res = {"result": True, "data": dic, "message": u"Get all packages successfully!"}
    return jsonify(res)


@push.route('/api/package', methods=['POST'])
@login_required
def upload_package():
    '''
    【API】处理上传文件，文件保存到本地并添加信息到数据库。
    :return:
    '''
    form = UploadForm()
    if form.validate_on_submit():
        filename = upload.save(form.upload_file.data, name=form.upload_file.data.filename)
        path = upload.path(filename)
        size = os.stat(path).st_size
        md5 = checksum(path)

        new_package = Package(
            filename=filename,
            size=size,
            md5=md5,
        )
        new_package.save()
        logger.info("{0} - Upload {1} package with id {2}".format(current_user.name, filename, new_package.id))
        return jsonify({"result": True, "data": None, "message": "upload the package file successfully"})
    err = form.errors
    logger.error("{0} - Fail to upload package because {1}".format(current_user.name, err))
    res = {"result": True, "data": None, "message": err}
    return jsonify(res)


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
        filename = package.filename
        path = upload.path(filename)
        os.remove(path)
        package.delete()
        logger.info("{0} - Delete {1} package with id {2}".format(current_user.name, filename, id))
        return jsonify({"result": True, "data": None, "message": "Delete the package successfully"})
    res_message = u"Failed! The package with id %s is not excisted" % id
    logger.error("{0} - {1}".format(current_user.name, res_message))
    return jsonify({"result": False, "data": None, "message": res_message})
