from flask import Flask
from pymongo import MongoClient
from pyes import ES

from config import *

app = Flask(__name__)
app.config.from_object('config')

mongo_conn = MongoClient(host = MONGODB_HOST, port = MONGODB_PORT)[MONGODB_DB]
es_conn = ES(ES_SERVER)

from app import views
