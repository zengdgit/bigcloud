# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

import os
from config import config
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# TODO 为啥要分割？
if __name__.find('.') > 0:
    flask_name = __name__.split('.')[0]
else:
    flask_name = __name__


class HackedSQLAlchemy(SQLAlchemy):
    """A simple hack to support isolation level"""

    def apply_driver_hacks(self, app, info, options):
        if app.config.get('SQLALCHEMY_ISOLATION_LEVEL'):
            options['isolation_level'] = app.config['SQLALCHEMY_ISOLATION_LEVEL']
        elif info.drivername.startswith('mysql'):
            options['isolation_level'] = 'READ COMMITTED'
        elif info.drivername == 'sqlite':
            options['isolation_level'] = 'READ UNCOMMITTED'
        super(HackedSQLAlchemy, self).apply_driver_hacks(app, info, options)


app = Flask(flask_name)
db = HackedSQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = ''


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)

    db.init_app(app)

    # register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint, url_prefix='/home')

    from .connect import connect as connect_blueprint
    app.register_blueprint(connect_blueprint, url_prefix='/connect')

    from .monitor import monitor as monitor_blueprint
    app.register_blueprint(monitor_blueprint, url_prefix='/monitor')

    from .push import push as push_blueprint
    app.register_blueprint(push_blueprint, url_prefix='/push')

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
