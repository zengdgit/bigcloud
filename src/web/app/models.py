# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '%s (%r, %r)' % (self.__class__.__name__, self.name, self.email)

    def save(self):
        db.session.add(self)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    # user_id is a unicode string, needed to be converted it to int
    return User.query.get(int(user_id))
