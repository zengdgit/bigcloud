# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/02/20 Chen Weijian : Init

import os


class MessageType(object):
    NULL = 'null'
    CONNECT = 'connect'
    SYNC_APP_GROUP = 'sync_app_group'
    SYNC_SETTING = 'sync_setting'


class ReceiveMessage(object):
    SUPPORT = [
        MessageType.CONNECT,
        MessageType.SYNC_APP_GROUP,
    ]

    @classmethod
    def support_message_type(cls, message):
        return message in ReceiveMessage.SUPPORT


class ResponseCode:
    SUCCESS = True
    FAIL = False


class ResponseMessage(object):
    @classmethod
    def create(cls, message_type=MessageType.NULL, message=None, result=ResponseCode.FAIL):
        return {
            'token': os.environ.get('BIG_CLOUD_TOKEN'),
            'type': message_type,
            'message': message,
            'result': result,
        }
