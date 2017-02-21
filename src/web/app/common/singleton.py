# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/02/21 Chen Weijian : Init

import threading


class Singleton(object):
    __instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if Singleton.__instance is None:
            with Singleton._lock:
                if Singleton.__instance is None:
                    Singleton.__instance = super(Singleton, cls).__new__(cls)
        return cls.__instance
