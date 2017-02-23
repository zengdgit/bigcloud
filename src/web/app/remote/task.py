# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/02/20 Chen Weijian : Init

import json

from .. import logger
from ..models import LittleCloud
from ..common.singleton import Singleton
from .push_message import PUSH_MESSAGE_MANAGER


class ResponseKey:
    RESULT = 'result'
    MESSAGE = 'msg'


class ResponseCode:
    SUCCESS = 'success'
    FAIL = 'fail'


class ResponseResult:
    FAIL = {
        ResponseKey.RESULT: ResponseCode.FAIL
    }

    SUCCESS = {
        ResponseKey.RESULT: ResponseCode.SUCCESS
    }


class ReceiveMessage(object):
    # for little cloud post data
    CONNECT = 'connect'
    # MONITOR = 'monitor'
    # VMMONITOR = 'vmmonitor'
    # EVENT = 'event'
    # TEMPLATE_LIST = 'template_list'

    # for little cloud get data
    GET_PUSH_TASK = 'get_push_task'
    APPLICATION_META = 'application_meta'
    USER_GROUP_INFO = 'user_group_info'
    DOWNLOAD_PACKAGE = 'download_package'

    @classmethod
    def support_message_type(cls, message):
        support = [
            ReceiveMessage.CONNECT,
            # ReceiveMessage.MONITOR,
            # ReceiveMessage.VMMONITOR,
            # ReceiveMessage.EVENT,
            # ReceiveMessage.TEMPLATE_LIST,
            ReceiveMessage.GET_PUSH_TASK,
            ReceiveMessage.APPLICATION_META,
            ReceiveMessage.USER_GROUP_INFO,
            ReceiveMessage.DOWNLOAD_PACKAGE
        ]
        return message in support


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
            if not littlecloud_id:
                logger.error('Auth fail for little cloud %s' % data['token'])
                return ResponseResult.FAIL

            message_type, message = cls._get_message(data)
            if ReceiveMessage.support_message_type(message_type):
                return eval(cls._classname(message_type) + 'Task.execute')(param=message, cloud_id=littlecloud_id)
            else:
                logger.error('Not support little cloud message %s.', message_type)
                return ResponseResult.FAIL
        except Exception as e:
            logger.error('Fail to process message %s.', message_type)
            return ResponseResult.FAIL

    @classmethod
    def _get_message_data(cls, request):
        return json.loads(request.data.decode())

    @classmethod
    def _authentication(cls, data):
        try:
            token = data['token']
            cloud_name = token
            little_cloud = LittleCloud.query.filter(LittleCloud.name == cloud_name,
                                                    LittleCloud.is_connectible == True).first()
            if not little_cloud:
                return None
            else:
                return little_cloud.id
        except Exception as e:
            logger.error('Authentication error for little cloud')
            return None

    @classmethod
    def _get_message(cls, data):
        return data['message_type'], data['message']

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
            return ResponseResult.FAIL
        return ResponseResult.SUCCESS


class GetPushTaskTask(BaseTask):
    @classmethod
    def process(cls, param, cloud_id):
        try:
            messages = PUSH_MESSAGE_MANAGER.pop_all_message(cloud_id)
            if messages:
                pass
            else:
                pass
            return messages
        except Exception as e:
            logger.error('Get message queue error for little cloud %s' % cloud_id)
