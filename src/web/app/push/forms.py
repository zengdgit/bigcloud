# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length,Required
from .. import upload


class UploadForm(FlaskForm):
    upload_file = FileField(validators=[
        FileAllowed(upload, u'只能上传图片！'),
        FileRequired(u'文件未选择！')])


class ApplicationForm(FlaskForm):
    name = StringField(id='name', validators=[DataRequired(), Length(1, 50)])
    first_classification_id = StringField(id='first_classification_id', validators=[DataRequired(), Length(1, 10)])
    secondary_classification_id = StringField(id='secondary_classification_id',
                                              validators=[DataRequired(), Length(1, 10)])
    function_id = StringField(id='function_id', validators=[DataRequired(), Length(1, 10)])
    language_id = StringField(id='language_id', validators=[DataRequired(), Length(1, 255)])
    os_id = StringField(id='os_id', validators=[DataRequired(), Length(1, 255)])
    cpu_id = StringField(id='cpu_id', validators=[DataRequired(), Length(1, 255)])
    package_id = StringField(id='package_id', validators=[DataRequired(), Length(1, 255)])
    install_command = StringField(id='install_command', validators=[DataRequired(), Length(1, 2083)])
    version = StringField(id='version', validators=[DataRequired(), Length(1, 255)])



class FunctionForm(FlaskForm):
    id = StringField(id='id', validators=[DataRequired()])
    name = StringField(id='name', validators=[DataRequired(), Length(1, 50)])
    secondary_classification_id = StringField(id='secondary_classification_id',
                                              validators=[DataRequired(), Length(1, 10)])



class AppGroupForm(FlaskForm):
    name = StringField(id='name', validators=[DataRequired(), Length(1, 50)])
    description = StringField(id='description', validators=[DataRequired(), Length(1, 50)])
    apps = StringField(id='apps', validators=[])


class TimetableForm(FlaskForm):
    name = StringField(id='name', validators=[DataRequired(), Length(1, 50)])
    course_num = IntegerField(id='course_num', validators=[DataRequired()])
    course_interval = IntegerField(id='course_interval', validators=[DataRequired()])
    start_time = DateTimeField(id='start_time', validators=[DataRequired])


class FlavorForm(FlaskForm):
    name = StringField(id='name', validators=[DataRequired(), Length(1, 50)])
    cpunum = IntegerField(id='cpunum', validators=[DataRequired()])
    ramnum = IntegerField(id='ramnum', validators=[DataRequired()])
    disknum = IntegerField(id='disknum', validators=[DataRequired()])