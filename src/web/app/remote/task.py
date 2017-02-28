# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/02/20 Chen Weijian : Init

import json

from .. import logger
from ..models import LittleCloud
from ..common.singleton import Singleton
from .message import MessageType, ReceiveMessage, ResponseCode, ResponseMessage


# class ResponseKey:
#     RESULT = 'result'
#     MESSAGE = 'msg'
#
#
# class ResponseCode:
#     SUCCESS = 'success'
#     FAIL = 'fail'
#
#
# class ResponseResult:
#     FAIL = {
#         ResponseKey.RESULT: ResponseCode.FAIL
#     }
#
#     SUCCESS = {
#         ResponseKey.RESULT: ResponseCode.SUCCESS
#     }


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


class SyncAppGroupInfoTask(BaseTask):
    @classmethod
    def process(cls, param, cloud_id):
        try:
            little_cloud = LittleCloud.query.get(int(cloud_id))
            # 检查小云是否已接入
            if not little_cloud.is_connected:
                return ResponseMessage.create(message_type=MessageType.SYNC_APP_GROUP, result=ResponseCode.FAIL)

            data = []
        except Exception as e:
            logger.error('ConnectProcessor error')
            return ResponseMessage.create(message_type=MessageType.SYNC_APP_GROUP, result=ResponseCode.FAIL)

        return ResponseMessage.create(message_type=MessageType.CONNECT, message=data, result=ResponseCode.SUCCESS)

# class GetPushTaskTask(BaseTask):
#     # !!!已放弃使用这个推送任务。
#     @classmethod
#     def process(cls, param, cloud_id):
#         try:
#             messages = PUSH_MESSAGE_MANAGER.pop_all_message(cloud_id)
#             if messages:
#                 pass
#             else:
#                 pass
#             return messages
#         except Exception as e:
#             logger.error('Get message queue error for little cloud %s' % cloud_id)
