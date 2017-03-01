# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

import os
import sys
import re

# Fix path problem
basedir = os.path.abspath(os.path.dirname(__file__))
os.chdir(basedir)
sys.path.append(basedir)
sys.path.append(os.path.join(basedir, '..'))

# Import environment variables
env_file_path = os.path.join(basedir, '.env')
if os.path.exists(env_file_path):
    print('Importing environment from .env...')
    env = {}
    for line in open(env_file_path):
        line = line.strip()
        # Skip comments
        if re.match('^\s*#', line):
            continue
        try:
            idx = line.index('=')
        except:
            continue
        if idx + 1 == len(line):
            continue
        env[line[:idx]] = line[idx + 1:]
    os.environ.update(env)

from app import app, db
from flask import redirect, url_for
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask_login import login_required

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
@login_required
def index():
    return redirect(url_for('home.index'))


@manager.command
def deploy():
    """Run deployment tasks."""
    from app.models import User, Function, Language, CPU, OS

    User.insert_default_users()
    Function.insert_default_functions()
    Language.insert_default_languages()
    CPU.insert_default_cpus()
    OS.insert_default_oses()


@manager.command
def runserver():
    app.debug = True
    app.run(host='0.0.0.0', port=5354)


if __name__ == '__main__':
    manager.run()
