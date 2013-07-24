from flask import Flask
from flask.ext.admin import Admin
from .admin import PaperView, ScholarPaperView
from pymongo import MongoClient
from pyes import ES
from redis import StrictRedis

from config import *

app = Flask(__name__)
app.config.from_object('config')
app.debug = DEBUG

mongo_conn = MongoClient(host = MONGODB_HOST, port = MONGODB_PORT)
es_conn = ES(ES_SERVER)
redis_conn = StrictRedis(host= REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

admin = Admin(app, name='Academi')
admin.add_view(PaperView(mongo_conn[PAPER_DB][PAPER_COLLECTION], name = 'Paper'))
admin.add_view(ScholarPaperView(mongo_conn[SCHOLAR_DB][SCHOLAR_PAPER_COLLECTION], name = 'Scholar'))

from app import views
