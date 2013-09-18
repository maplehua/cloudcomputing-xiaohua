from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongoengine.panels import MongoDebugPanel
from flask.ext.login import LoginManager
from flask.ext.admin import Admin
from .admin import config_admin
from pymongo import MongoClient
from pyes import ES

from config import *

app = Flask(__name__)
app.config.from_object('config')

# debug
app.debug = DEBUG
app.config['DEBUG_TB_PANELS'] = ('flask.ext.mongoengine.panels.MongoDebugPanel',)
#toolbar = DebugToolbarExtension(app)

# database connection
mongo_conn = MongoClient(host = MONGODB_HOST, port = MONGODB_PORT)
es_conn = ES(ES_SERVER)
app.config['MONGODB_SETTINGS'] = {'DB': 'academi',
        'HOST': '10.77.20.50',
        'PORT': 27017}
mongo_db = MongoEngine(app)

# flask login
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login'

# flask admin
if ADMIN:
    admin = config_admin()
    admin.init_app(app)

from app import views

# jinja costum filter
def rm_num_at_end(name):
    import re
    result = re.sub("\s\d+$","",name)
    return result
env = app.jinja_env
env.filters['rm_end_num'] = rm_num_at_end
