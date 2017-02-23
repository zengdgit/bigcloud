# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

import os
from flask import Flask, request, jsonify, render_template, url_for, redirect
from . import push
from ..models import Package, Application, OS, Language, CPU, FirstClassification, SecondaryClassification, Function, \
    AppGroup
from ..utils import checksum
from flask_login import login_required, current_user

from .forms import UploadForm, ApplicationForm, FunctionForm, AppGroupForm

from .. import upload, logger


@push.route('/')
@login_required
def index():
    return redirect(url_for('push.littlecloud'))


@push.route('/littlecloud')
@login_required
def littlecloud():
    return render_template('push/push_littlecloud.html')


@push.route('/appgroup')
@login_required
def appgroup():
    return render_template('push/push_appgroup.html')


@push.route('/application')
@login_required
def application():
    return render_template('push/push_application.html')


@push.route('/package')
@login_required
def package():
    return render_template('push/push_package.html')


@push.route('/function')
@login_required
def function():
    return render_template('push/push_function.html')


#################
# function
#################
@push.route('/api/function', methods=['GET'])
@login_required
def get_all_functions():
    '''
    【API】得到所有功能的数据。
    :return:
    '''
    function = Function.query.all()
    dic = []

    for i in function:
        secondary_classification = SecondaryClassification.query.filter_by(id=i.secondary_classification_id).first()
        first_classification = FirstClassification.query.filter_by(
            id=SecondaryClassification.first_classification_id).first()
        item = {
            "id": i.id,
            "name": i.name,
            "first_classification": first_classification.name,
            "secondary_classification": secondary_classification.name,
        }
        dic.append(item)
    logger.info("{0} - Get all function".format(current_user.name))
    res = {"result": True, "data": dic, "message": u"Get all function successfully!"}

    return jsonify(res)


@push.route('/api/function', methods=['POST'])
@login_required
def create_function():
    form = FunctionForm()

    if form.validate_on_submit():
        # id=form.id.data
        new_function = Function(
            id=int(form.id.data),
            name=form.name.data,
            secondary_classification_id=form.secondary_classification_id.data
        )
        new_function.save()

        # logger.info("{0} - Add {1} function with id {2}".format(current_user.name))
        return jsonify({"result": True, "data": None, "message": u"Add new function successfully"})
    error = form.errors
    logger.error("{0} - Fail to add function because {1}".format(current_user.name, error))
    return jsonify({"result": False, "data": None, "message": error})


@push.route('/api/function/<int:id>', methods=['DELETE'])
def delete_Function_by_id(id):
    '''
    【API】根据 id 删除功能。
    :param id: 应用 ID
    :return:
    '''
    function = Function.query.get(int(id))
    if function:
        name = function.name
        function.delete()
        logger.info("{0} - Delete {1} application with id {2}".format(current_user.name, name, id))
        return jsonify({"result": True, "data": None, "message": "Delete the function successfully"})
    res_message = u"Failed! The function with id %s is not excisted" % id
    logger.error("{0} - {1}".format(current_user.name, res_message))
    return jsonify({"result": False, "data": None, "message": res_message})


@push.route('/api/function/<int:id>', methods=['PUT'])
@login_required
def update_function_by_id(id):
    '''
    【API】根据 id 更新功能。
    :param id: 应用 ID
    :return:
    '''
    form = FunctionForm()
    if form.validate_on_submit():
        function = Function.query.get(int(id))
        if function:
            function.id = form.id.data
            function.name = form.name.data
            function.secondary_classification_id = form.secondary_classification_id.data
            function.save()
            logger.info(
                "{0} - Update {1} function with id {2}".format(current_user.name, function.name, function.id))
            return jsonify({"result": True, "data": None, "message": u"Edit new function successfully"})
        res_message = u"Failed! The function with id %s is not excisted" % id
        logger.error("{0} - {1}".format(current_user.name, res_message))
        return jsonify({"result": False, "data": None, "message": res_message})

    error = form.errors
    logger.error("{0} - Fail to update function because {1}".format(current_user.name, error))
    return jsonify({"result": False, "data": None, "message": error})


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
    data = []
    for i in packages:
        item = {
            "id": i.id,
            "filename": i.filename,
            "url": upload.url(i.filename),
            "size": i.size,
            "md5": i.md5,
        }
        data.append(item)
    # logger.info("{0} - Get all packages".format(current_user.name))
    res = {"result": True, "data": data, "message": u"Get all packages successfully!"}
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


#################
# application
#################
@push.route('/api/first_classification', methods=['GET'])
@login_required
def get_all_first_classification():
    '''
    【API】得到所有一级分类的数据。
    :return:
    '''
    first_classification = FirstClassification.query.all()
    data = {}
    for i in first_classification:
        data[i.id] = i.name
    res = {"result": True, "data": data, "message": u"Get all first classification successfully!"}
    return jsonify(res)


@push.route('/api/first_classification/<int:id>/secondary_classification', methods=['GET'])
@login_required
def get_all_secondary_classification_by_first_classification_id(id):
    '''
    【API】根据一级分类的 ID 得到对应的二级分类。
    :param id: 一级分类 ID
    :return:
    '''
    secondary_classification = SecondaryClassification.query.filter(
        SecondaryClassification.first_classification_id == id).all()
    data = {}
    for i in secondary_classification:
        data[i.id] = i.name
    res = {"result": True, "data": data, "message": u"Get secondary classification successfully!"}
    return jsonify(res)


@push.route('/api/secondary_classification/<int:id>/function', methods=['GET'])
@login_required
def get_all_function_by_secondary_classification_id(id):
    '''
    【API】根据二级分类的 ID 得到对应的三级分类。
    :param id: 二级分类 ID
    :return:
    '''
    function = Function.query.filter(Function.secondary_classification_id == id).all()
    data = {}
    for i in function:
        data[i.id] = i.name
    res = {"result": True, "data": data, "message": u"Get function successfully!"}
    return jsonify(res)


@push.route('/api/language', methods=['GET'])
@login_required
def get_all_languages():
    '''
    【API】得到所有语言的数据。
    :return:
    '''
    languages = Language.query.all()
    data = {}
    for i in languages:
        data[i.id] = i.name
    res = {"result": True, "data": data, "message": u"Get all languages successfully!"}
    return jsonify(res)


@push.route('/api/os', methods=['GET'])
@login_required
def get_all_OS():
    '''
    【API】得到所有操作系统的数据。
    :return:
    '''
    os = OS.query.all()
    data = {}
    for i in os:
        data[i.id] = i.name
    res = {"result": True, "data": data, "message": u"Get all OS successfully!"}
    return jsonify(res)


@push.route('/api/cpu', methods=['GET'])
@login_required
def get_all_CPU():
    '''
    【API】得到所有CPU的数据。
    :return:
    '''
    cpu = CPU.query.all()
    data = {}
    for i in cpu:
        data[i.id] = i.name
    res = {"result": True, "data": data, "message": u"Get all CPU successfully!"}
    return jsonify(res)


@push.route('/api/application', methods=['GET'])
@login_required
def get_all_applications():
    '''
    【API】得到所有应用的数据。
    :return:
    '''
    applications = Application.query.all()
    data = []
    for i in applications:
        item = {
            "id": i.id,
            "name": i.name,
            "version": i.version,
            "secondary_classification": i.function.secondary_classification.name if i.function else "",
            "function": i.function.name if i.function else "",
            "os": i.os.name if i.os else "",
            "cpu": i.cpu.name if i.cpu else "",
            "language": i.language.name if i.language else "",
            "install_command": i.install_command,
            "package": i.package.filename if i.package else "",
            "first_classification_id": i.function.secondary_classification.first_classification.id if i.function else "",
            "secondary_classification_id": i.function.secondary_classification.id if i.function else "",
            "function_id": i.function_id,
            "os_id": i.os_id,
            "cpu_id": i.cpu_id,
            "language_id": i.language_id,
            "package_id": i.package_id,
        }
        data.append(item)
    # logger.info("{0} - Get all applications".format(current_user.name))
    res = {"result": True, "data": data, "message": u"Get all applications successfully!"}
    return jsonify(res)


@push.route('/api/application', methods=['POST'])
@login_required
def add_application():
    '''
    【API】添加应用。
    :return:
    '''
    form = ApplicationForm()
    if form.validate_on_submit():
        name = form.name.data
        new_application = Application(
            name=form.name.data,
            version=form.version.data,
            function_id=form.function_id.data,
            language_id=form.language_id.data,
            cpu_id=form.cpu_id.data,
            os_id=form.os_id.data,
            package_id=form.package_id.data,
            install_command=form.install_command.data,
        )
        new_application.save()
        logger.info("{0} - Add {1} application with id {2}".format(current_user.name, name, new_application.id))
        return jsonify({"result": True, "data": None, "message": "Add the application successfully"})
    err = form.errors
    logger.error("{0} - Fail to add application because {1}".format(current_user.name, err))
    res = {"result": True, "data": None, "message": err}
    return jsonify(res)


@push.route('/api/application/<int:id>', methods=['PUT'])
@login_required
def update_application_by_id(id):
    '''
    【API】根据 id 更新应用。
    :param id: 应用 ID
    :return:
    '''
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application.query.get(int(id))
        if application:
            application.name = form.name.data
            application.version = form.version.data
            application.function_id = form.function_id.data
            application.language_id = form.language_id.data
            application.cpu_id = form.cpu_id.data
            application.os_id = form.os_id.data
            application.package_id = form.package_id.data
            application.install_command = form.install_command.data
            application.save()
            logger.info(
                "{0} - Update {1} application with id {2}".format(current_user.name, application.name, application.id))
            return jsonify({"result": True, "data": None, "message": u"Edit new application successfully"})
        res_message = u"Failed! The application with id %s is not excisted" % id
        logger.error("{0} - {1}".format(current_user.name, res_message))
        return jsonify({"result": False, "data": None, "message": res_message})

    error = form.errors
    logger.error("{0} - Fail to update application because {1}".format(current_user.name, error))
    return jsonify({"result": False, "data": None, "message": error})


@push.route('/api/application/<int:id>', methods=['DELETE'])
@login_required
def delete_Application_by_id(id):
    '''
    【API】根据 id 删除应用。
    :param id: 应用 ID
    :return:
    '''
    application = Application.query.get(int(id))
    if application:
        name = application.name
        application.delete()
        logger.info("{0} - Delete {1} application with id {2}".format(current_user.name, name, id))
        return jsonify({"result": True, "data": None, "message": "Delete the application successfully"})
    res_message = u"Failed! The application with id %s is not excisted" % id
    logger.error("{0} - {1}".format(current_user.name, res_message))
    return jsonify({"result": False, "data": None, "message": res_message})


#################
# appgroup
#################
@push.route('/api/appgroup', methods=['GET'])
@login_required
def get_all_appgroups():
    '''
    【API】得到所有应用组的数据。
    :return:
    '''
    groups = AppGroup.query.all()
    data = []
    for i in groups:
        apps = []
        for a in i.applications:
            apps.append({"id": a.id, "name": a.name})
        item = {
            "id": i.id,
            "name": i.name,
            "description": i.description,
            "apps": apps,
        }
        data.append(item)
    res = {"result": True, "data": data, "message": u"Get all applications successfully!"}
    return jsonify(res)


@push.route('/api/appgroup', methods=['POST'])
@login_required
def add_appgroup():
    '''
    【API】添加应用组。
    :return:
    '''
    form = AppGroupForm()
    if form.validate_on_submit():
        name = form.name.data
        apps_id = form.apps.raw_data
        apps = []
        for id in apps_id:
            application = Application.query.get(int(id))
            if application:
                apps.append(application)
        new_appgroup = AppGroup(
            name=form.name.data,
            description=form.description.data,
            applications=apps,
        )
        new_appgroup.save()
        logger.info("{0} - Add {1} appgroup with id {2}".format(current_user.name, name, new_appgroup.id))
        return jsonify({"result": True, "data": None, "message": "Add the appgroup successfully"})
    err = form.errors
    logger.error("{0} - Fail to add appgroup because {1}".format(current_user.name, err))
    res = {"result": True, "data": None, "message": err}
    return jsonify(res)


@push.route('/api/appgroup/<int:id>', methods=['PUT'])
@login_required
def update_appgroup_by_id(id):
    '''
    【API】根据 id 更新应用组。
    :param id: 应用组 ID
    :return:
    '''
    form = AppGroupForm()
    if form.validate_on_submit():
        group = AppGroup.query.get(int(id))
        if group:
            apps_id = form.apps.raw_data
            apps = []
            for app_id in apps_id:
                application = Application.query.get(int(app_id))
                if application:
                    apps.append(application)

            group.name = form.name.data
            group.description = form.description.data
            group.applications = apps
            group.save()
            logger.info(
                "{0} - Update {1} appgroup with id {2}".format(current_user.name, group.name, group.id))
            return jsonify({"result": True, "data": None, "message": u"Edit new appgroup successfully"})
        res_message = u"Failed! The appgroup with id %s is not excisted" % id
        logger.error("{0} - {1}".format(current_user.name, res_message))
        return jsonify({"result": False, "data": None, "message": res_message})

    error = form.errors
    logger.error("{0} - Fail to update appgroup because {1}".format(current_user.name, error))
    return jsonify({"result": False, "data": None, "message": error})


@push.route('/api/appgroup/<int:id>', methods=['DELETE'])
@login_required
def delete_AppGroup_by_id(id):
    '''
    【API】根据 id 删除应用组。
    :param id: 应用组 ID
    :return:
    '''
    group = AppGroup.query.get(int(id))
    if group:
        name = group.name
        group.delete()
        logger.info("{0} - Delete {1} appgroup with id {2}".format(current_user.name, name, id))
        return jsonify({"result": True, "data": None, "message": "Delete the appgroup successfully"})
    res_message = u"Failed! The appgroup with id %s is not excisted" % id
    logger.error("{0} - {1}".format(current_user.name, res_message))
    return jsonify({"result": False, "data": None, "message": res_message})
