import scrypt
import datetime

from datetime import timedelta
from app import app, db
from app.models import *
from app.api import *

from flask.ext.script import Manager, Server, prompt_bool

manager = Manager(app)


@manager.command
def syncdb():
    '''
    Create a new db.
    `python manage.py createdb`
    '''
    db.create_all()

@manager.command
def createdb():
    '''
    Create a new db.
    `python manage.py createdb`
    '''
    db.create_all()

@manager.command
def dropdb():
    '''
    Kill off the darn db and start over
    `python manage.py dropdb`
    '''
    if prompt_bool('Are you sure you want to lose all your data'):
        db.drop_all()

@manager.command
def reloaddb():
    dropdb()
    createdb()


if __name__ == '__main__':
    manager.run()
