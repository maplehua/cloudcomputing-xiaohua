#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, json
from pprint import pprint
from pyes import ES
from pymongo import MongoClient

from config import *

es_conn = ES(server = ES_SERVER)
mongo_conn = MongoClient(host = MONGODB_HOST, port = MONGODB_PORT)

def mongo_init_db(db, collection):
    mongo_conn[db].drop_collection(collection)
    print "mongodb [%s] drop collection '%s.%s'" % (MONGODB_SERVER, db, collection)
    mongo_conn[db].create_collection(collection)
    print "mongodb [%s] create collection '%s.%s'" % (MONGODB_SERVER, db, collection)

def mongo_create_index(db, collection, key_or_list):
    mongo_conn[db][collection].create_index(key_or_list)
    print "mongodb [%s] create index on '%s.%s - %s'" % (MONGODB_SERVER, db, collection, key_or_list)

def es_init_index(index):
    es_conn.indices.delete_index_if_exists(index)
    print "elasticsearch [%s] drop index '%s'" % (ES_SERVER, index)
    es_conn.indices.create_index_if_missing(index)
    print "elasticsearch [%s] create index '%s'" % (ES_SERVER, index)

def es_put_mapping(index, doc_type, mapping):
    #es_conn.indices.delete_mapping(index = index, doc_type = doc_type)
    #print "elasticsearch [%s] drop mapping '%r'" % (ES_SERVER, mapping)
    es_conn.indices.put_mapping(doc_type = doc_type, mapping = {'properties':mapping}, indices = index)
    print "elasticsearch [%s] create mapping '%r'" % (ES_SERVER, mapping)

def init_paper():
    mongo_init_db(db = MONGODB_DB, collection = PAPER_COLLECTION)
    mongo_create_index(db = MONGODB_DB, collection = PAPER_COLLECTION, key_or_list = 'uuid')
    es_init_index(index = PAPER_INDEX)
    es_put_mapping(index = PAPER_INDEX, doc_type = PAPER_TYPE, mapping = PAPER_MAPPING)

def init_paper_en():
    mongo_init_db(db = MONGODB_DB, collection = PAPER_EN_COLLECTION)
    mongo_create_index(db = MONGODB_DB, collection = PAPER_EN_COLLECTION, key_or_list = 'uuid')
    es_init_index(index = PAPER_EN_INDEX)
    es_put_mapping(index = PAPER_EN_INDEX, doc_type = PAPER_EN_TYPE, mapping = PAPER_EN_MAPPING)

if __name__ == '__main__':
    init_paper_en()
    init_paper()
