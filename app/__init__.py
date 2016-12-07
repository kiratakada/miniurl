import redis

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app.middleware import ReverseProxied

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

app.config.from_object('config')
db = SQLAlchemy(app)

app.kvs = redis.StrictRedis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DB'],
    #password=app.config['REDIS_DB_PASS']
)

from app import api
from app import models
