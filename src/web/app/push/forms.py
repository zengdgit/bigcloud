
# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

from flask_wtf import FlaskForm,Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from .. import upload
from wtforms import StringField,SelectField, SelectMultipleField
from wtforms.validators import data_required, length, regexp, number_range, Email, EqualTo
from ..models import FirstClassification,SecondaryClassification


# def choice_of_first():
#    firsts = FirstClassification.query.all()
#    return [(first.id,first.name) for first in firsts]
#
#
# def choice_of_secondary():
#     secondarys = SecondaryClassification.query.all()
#     return [(secondary.id,secondary.name) for secondary in secondarys]

class UploadForm(FlaskForm):
    upload_file = FileField(validators=[
        FileAllowed(upload, u'只能上传图片！'),
        FileRequired(u'文件未选择！')])

class FunctionCreateForm(FlaskForm):

    id = StringField('id',validators=[data_required()])
    name = StringField('name', validators=[data_required(),
        length(1, 64, message='用户名过长')])
    # first_classification = SelectField('一级分类', choices=[],coerce=str, default=None)
    # secondary_classification = SelectField('二级分类', choices=[], coerce=str,default=None)
    #
    # def __init__(self, *args, **kwargs):
    #     super(FunctionCreateForm, self).__init__(*args, **kwargs)
    #     self.first_classification.choices = choice_of_first()
    #     self.secondary_classification.choices = choice_of_secondary()