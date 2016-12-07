import base64
import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://kiratakada:p@ssw0rd24@127.0.0.1/miniurl_db'

DATABASE_CONNECT_OPTIONS = {}
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_PASS = "kiratak#Pvee"

THREADS_PER_PAGE = 8
CSRF_ENABLED = False

SHORTEN_BASE = 'http://get.scp4.me/'
SHORTEN_SALT = 'scp4kiradidime'

try:
    from local_config import *
except ImportError:
    pass
