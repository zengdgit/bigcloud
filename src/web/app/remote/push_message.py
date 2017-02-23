# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/02/20 Chen Weijian : Init

import queue
import os

from .. import logger
from ..common.singleton import Singleton


class PushMessage(object):
    PUSH_GROUP_APP_TEMPLATE = 'push_group_app_template'

    @classmethod
    def create(cls, little_cloud, message_type, message):
        # TODO 暂时不确定Sequence的具体作用
        # sequence = Sequence(little_cloud=little_cloud)
        # sequence.save()
        return {
            'token': os.environ.get('BIG_CLOUD_TOKEN'),
            'message_type': message_type,
            'message': message,
            # 'sequence': sequence.next_sequence - 1
        }


class PushMessageManager(Singleton):
    """
    message manager
    """

    def __init__(self):
        self.message_queue = {}

    def put_message(self, cloud_id, message):
        try:
            self._lock.acquire()
            cloud_queue = self.message_queue.get(cloud_id)
            if not cloud_queue:
                self.message_queue[cloud_id] = queue.Queue(maxsize=os.environ.get('MESSAGE_QUEUE_SIZE'))
            self.message_queue[cloud_id].put(message)
        except Exception as e:
            logger.error('Put message queue for little cloud %s error' % cloud_id)
        finally:
            self._lock.release()

    def pop_message(self, cloud_id):
        try:
            self._lock.acquire()
            if self.message_queue.get(cloud_id):
                return self.message_queue[cloud_id].get()
        except Exception as e:
            logger.error('get message from queue of little cloud %s error' % cloud_id)
        finally:
            self._lock.release()

    def pop_all_message(self, cloud_id):
        try:
            queue_size = self.message_queue[cloud_id].qsize()
            message_list = []
            for i in range(queue_size):
                message_list.append(self.message_queue[cloud_id].get())
            return message_list
            # return [item for item in self.message_queue[cloud_id]]

        except Exception as e:
            pass


PUSH_MESSAGE_MANAGER = PushMessageManager()
