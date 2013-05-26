#!/usr/bin/python
# -*- coding: utf-8 -*-
import settings
if settings.LIB_PATH:
    import sys
    sys.path.append(settings.LIB_PATH)

import requests
from pyes import *
from settings import paper_mapping

es_server = settings.ES_SETTING['server']

def init_index(es_server = '127.0.0.1:9200', index = 'test_index'):
    conn = ES(es_server)
    if not conn.exists_index(index):
        conn.indices.create_index(index)

def set_mapping(es_server = '127.0.0.1:9200', index = 'test_index', doc_type = 'test_type', mapping = None):
    conn = ES(es_server)
    conn.indices.put_mapping(doc_type, {'properties':mapping}, index)

def set_mongo_river(mongo_server = "127.0.0.1:27017",
        mongo_db = "test", mongo_collection = "test",
        es_server = "127.0.0.1:9200",
        es_index = "test", es_type = "test"):

    mongo_host = mongo_server.split(':')[0]
    mongo_port = mongo_server.split(':')[1]

    meta = '''
        {
            "type": "mongodb",
            "mongodb":{
                "servers":[
                        {
                            "host": "%s",
                            "port": "%s"
                        }
                    ],
                "db":"%s",
                "collection":"%s"
                },
            "index":{
                "name":"%s",
                "type":"%s"
                }
        }
    ''' % (mongo_host, mongo_port, mongo_db, mongo_collection, es_index, es_type)
    url = 'http://%s/_river/river-mongodb/_meta' % (es_server)
    r = requests.put(url, meta)
    print r.json()

if __name__=='__main__':
    init_index(es_server, index)
    set_mapping(es_server, index, doc_type = "test_type", mapping = paper_mapping)
    set_mongo_river(mongo_server, mongo_db = "academi", mongo_collection = "paper", es_server = "10.77.20.50:9200", es_index = "mongo_index", es_type = "test_type")
