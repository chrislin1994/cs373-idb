# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# configure sqlalchemy
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/free_spirits'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
