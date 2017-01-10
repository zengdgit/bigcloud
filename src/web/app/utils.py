# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

import hashlib


def checksum(filepath):
    try:
        md5 = hashlib.md5()
        file_obj = open(filepath, 'r+b')
        for chunk in iter(lambda: file_obj.read(128 * md5.block_size), b''):
            md5.update(chunk)
        file_obj.close()
        return md5.hexdigest().upper()
    except Exception as e:
        return None
