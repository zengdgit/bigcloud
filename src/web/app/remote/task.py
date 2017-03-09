# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/02/20 Chen Weijian : Init

import json

from .. import logger
from ..models import LittleCloud
from ..common.singleton import Singleton
from .message import MessageType, ReceiveMessage, ResponseCode, ResponseMessage


class TaskBroker(object):
    """
    message broker for message processing
    """

    @classmethod
    def dispatch(cls, request):
        message_type, message = None, None
        try:
            data = cls._get_message_data(request)
            littlecloud_id = cls._authentication(data)
            # 检查小云是否具有可接入的权限
            if not littlecloud_id:
                logger.error('Auth fail for little cloud %s' % data['token'])
                return ResponseMessage.create(result=ResponseCode.FAIL)

            message_type, message = cls._get_message(data)
            if ReceiveMessage.support_message_type(message_type):
                return eval(cls._classname(message_type) + 'Task.execute')(param=message, cloud_id=littlecloud_id)
            else:
                logger.error('Not support little cloud message %s.', message_type)
                return ResponseMessage.create(result=ResponseCode.FAIL)
        except Exception as e:
            logger.error('Fail to process message %s.', message_type)
            return ResponseMessage.create(result=ResponseCode.FAIL)

    @classmethod
    def _get_message_data(cls, request):
        return json.loads(request.data.decode())

    @classmethod
    def _authentication(cls, data):
        try:
            token = data['token']
            cloud_name = token
            little_cloud = LittleCloud.query.filter_by(name=cloud_name, is_connectible=True).first()
            if not little_cloud:
                return None
            else:
                return little_cloud.id
        except Exception as e:
            logger.error('Authentication error for little cloud')
            return None

    @classmethod
    def _get_message(cls, data):
        return data['type'], data['message']

    @classmethod
    def _classname(cls, message):
        return message.title().replace('_', '')


class BaseTask(Singleton):
    @classmethod
    def execute(cls, param, cloud_id):
        return cls.process(param, cloud_id)

    @classmethod
    def process(cls, param, cloud_id):
        pass


class ConnectTask(BaseTask):
    @classmethod
    def process(cls, param, cloud_id):
        try:
            little_cloud = LittleCloud.query.get(int(cloud_id))
            if not little_cloud.is_connected:
                little_cloud.is_connected = True
                little_cloud.save()
        except Exception as e:
            logger.error('ConnectProcessor error')
            return ResponseMessage.create(message_type=MessageType.CONNECT, result=ResponseCode.FAIL)

        return ResponseMessage.create(message_type=MessageType.CONNECT, result=ResponseCode.SUCCESS)


class SyncAppGroupTask(BaseTask):
    @classmethod
    def process(cls, param, cloud_id):
        try:
            little_cloud = LittleCloud.query.get(int(cloud_id))
            # 检查小云是否已接入
            if not little_cloud.is_connected:
                return ResponseMessage.create(message_type=MessageType.SYNC_APP_GROUP, result=ResponseCode.FAIL)

            data = []
            all_groups = little_cloud.appgroups
            for group in all_groups:
                all_applications = group.applications
                all_applications_info = []
                for app in all_applications:
                    app_info = {
                        'name': app.name,
                        'version': app.version,
                        'function': app.function.name if app.function else None,
                        'os': app.os.name if app.os else None,
                        'cpu': app.cpu.name if app.cpu else None,
                        'language': app.language.name if app.language else None,
                        'install_command': app.install_command,
                        'package': {
                            'filename': app.package.filename,
                            'size': app.package.size,
                            'md5': app.package.md5,
                        } if app.package else None,
                    }
                    all_applications_info.append(app_info)
                group_info = {
                    'name': group.name,
                    'description': group.description,
                    'applications': all_applications_info,
                }
                data.append(group_info)
        except Exception as e:
            logger.error('ConnectProcessor error')
            return ResponseMessage.create(message_type=MessageType.SYNC_APP_GROUP, result=ResponseCode.FAIL)

        return ResponseMessage.create(message_type=MessageType.SYNC_APP_GROUP, message=data,
                                      result=ResponseCode.SUCCESS)


class SyncSettingTask(BaseTask):
    from .utils import sync_timetable, sync_flavor
    sync_handler = {'timetable':sync_timetable, 'flavor':sync_flavor}
    @classmethod
    def process(cls, param, cloud_id):
        try:
            little_cloud = LittleCloud.query.get(int(cloud_id))
            # 检查小云是否已接入
            if not little_cloud.is_connected:
                return ResponseMessage.create(message_type=MessageType.SYNC_SETTING, result=ResponseCode.FAIL)
            logger.info(param['latest_setting'])
            data = cls.sync_handler[param['type']](param['latest_setting'])
            logger.info(data)
            return ResponseMessage.create(message_type=MessageType.SYNC_SETTING, message=data, result=ResponseCode.SUCCESS)
        except Exception as e:
            logger.error(param)
            import traceback
            traceback.print_exc()
            logger.error('sync %s templates error' % param['type'])
            return ResponseMessage.create(message_type=MessageType.SYNC_SETTING, result=ResponseCode.FAIL)