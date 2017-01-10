# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from .. import upload

class UploadForm(FlaskForm):
    upload_file = FileField(validators=[
        FileAllowed(upload, u'只能上传图片！'),
        FileRequired(u'文件未选择！')])
