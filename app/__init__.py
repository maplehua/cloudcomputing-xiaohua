from flask import Flask
from pymongo import MongoClient
from pyes import ES
from redis import StrictRedis

from config import *

app = Flask(__name__)
app.config.from_object('config')
app.debug = DEBUG

mongo_conn = MongoClient(host = MONGODB_HOST, port = MONGODB_PORT)[MONGODB_DB]
es_conn = ES(ES_SERVER)
redis_conn = StrictRedis(host= REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

from app import views
