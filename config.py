import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'my_precious'
SECURITY_PASSWORD_SALT = 'my_precious_two'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'database.db')
DATABASE_CONNECT_OPTIONS = {}
