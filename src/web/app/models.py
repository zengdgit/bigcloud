# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

import datetime
from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import EmailType, IPAddressType


##################
# auth
##################
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('用户名', db.String(50), unique=True)
    email = db.Column('邮箱', db.String(120))
    password_hash = db.Column('哈希加密密码', db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    # user_id is a unicode string, needed to be converted it to int
    return User.query.get(int(user_id))


#################
# connect
#################
class ProtocolType(object):
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'


class LittleCloud(db.Model):
    __tablename__ = 'littleclouds'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('小云平台名称', db.Unicode(255), unique=True)
    url = db.Column('小云平台URL', db.String(255), unique=True)
    is_connectible = db.Column('是否允许接入', db.Boolean, default=False)
    is_connected = db.Column('是否已经接入', db.Boolean, default=False)
    phone = db.Column('联系电话', db.String(30), nullable=True)
    email = db.Column('联系邮箱', EmailType, nullable=True)
    ip = db.Column('接入IP', IPAddressType, nullable=True)
    port = db.Column('接入端口', db.Integer, nullable=True)
    protocol = db.Column('接入协议', db.String(20), default=ProtocolType.HTTP)
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<LittleCloud %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


#################
# push
#################
class Package(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column('文件名', db.Unicode(255), unique=True)
    size = db.Column('文件总大小', db.Integer, default=0)
    md5 = db.Column('MD5', db.String(255), default='MD5')
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Package %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class FirstClassification(db.Model):
    __tablename__ = 'firstClassifications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('一级分类名', db.Unicode(255), unique=True)
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)
    secondary_classifications = db.relationship('SecondaryClassification', backref='firstClassifications',
                                                lazy='dynamic')

    def __repr__(self):
        return '<FirstClassification %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class SecondaryClassification(db.Model):
    __tablename__ = 'secondaryClassifications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('二级分类名', db.Unicode(255), unique=True)
    first_classification = db.Column(db.Integer, db.ForeignKey('firstClassifications.id'))
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)
    functions = db.relationship('Function', backref='secondaryClassifications', lazy='dynamic')

    def __repr__(self):
        return '<SecondaryClassification %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Function(db.Model):
    __tablename__ = 'functions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('功能名', db.Unicode(255), unique=True)
    secondary_classification = db.Column(db.Integer, db.ForeignKey('secondaryClassifications.id'))
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Function %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
