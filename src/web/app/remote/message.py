# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/02/20 Chen Weijian : Init

import queue
import os

from .. import logger
from ..common.singleton import Singleton


class MessageType(object):
    NULL = 'null'

    # for little cloud post data
    CONNECT = 'connect'
    # MONITOR = 'monitor'
    # VMMONITOR = 'vmmonitor'
    # EVENT = 'event'
    # TEMPLATE_LIST = 'template_list'

    # for little cloud get data
    SYNC_APP_GROUP = 'sync_app_group'

    # GET_PUSH_TASK = 'get_push_task'
    # APPLICATION_META = 'application_meta'
    # USER_GROUP_INFO = 'user_group_info'
    # DOWNLOAD_PACKAGE = 'download_package'


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


# class PushMessageManager(Singleton):
#     """
#     message manager
#     """
#
#     def __init__(self):
#         self.message_queue = {}
#
#     def put_message(self, cloud_id, message):
#         try:
#             self._lock.acquire()
#             cloud_queue = self.message_queue.get(cloud_id)
#             if not cloud_queue:
#                 self.message_queue[cloud_id] = queue.Queue(maxsize=os.environ.get('MESSAGE_QUEUE_SIZE'))
#             self.message_queue[cloud_id].put(message)
#         except Exception as e:
#             logger.error('Put message queue for little cloud %s error' % cloud_id)
#         finally:
#             self._lock.release()
#
#     def pop_message(self, cloud_id):
#         try:
#             self._lock.acquire()
#             if self.message_queue.get(cloud_id):
#                 return self.message_queue[cloud_id].get()
#         except Exception as e:
#             logger.error('get message from queue of little cloud %s error' % cloud_id)
#         finally:
#             self._lock.release()
#
#     def pop_all_message(self, cloud_id):
#         try:
#             queue_size = self.message_queue[cloud_id].qsize()
#             message_list = []
#             for i in range(queue_size):
#                 message_list.append(self.message_queue[cloud_id].get())
#             return message_list
#             # return [item for item in self.message_queue[cloud_id]]
#
#         except Exception as e:
#             pass
#
#
# PUSH_MESSAGE_MANAGER = PushMessageManager()
