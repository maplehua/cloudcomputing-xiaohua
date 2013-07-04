#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
from uuid import uuid1
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pyes import ES

from config import *

es_conn = ES(server = ES_SERVER)
mongo_conn = MongoClient(host = MONGODB_HOST, port = MONGODB_PORT)[MONGODB_DB]

def load_dir(path, file_type,parse_func, collection, index, doc_type):
    for root, dirs, files in os.walk(path):
        for f in files:
            if file_type == f[-len(file_type):]:
                print os.path.join(root, f)
                (mongo_doc, es_doc) = parse_func(os.path.join(root, f))
                print 'mongo - %r' % (import_mongo(mongo_doc, collection))
                print 'elasticsearch - %r' % (import_es(es_doc, index, doc_type))


def paper_xml_to_doc(infile):
    paper = BeautifulSoup(open(infile))

    uuid = unicode(uuid1())

    title = paper.title.get_text()
    publication = paper.conference.get_text()
    year = paper.year.get_text()
    body = paper.body.get_text()

    authors = []
    author_list = paper.find_all('author')
    for a in author_list:
        authors.append(a.get_text())

    mongo_doc = dict(uuid = uuid, title = title, authors = authors, publication = publication, year = year, body = body)
    es_doc = dict(uuid = uuid, title = title, body = body)
    return (mongo_doc, es_doc)

def import_mongo(doc, collection):
    return mongo_conn[collection].insert(doc)

def import_es(doc, index, doc_type):
    return es_conn.index(doc = doc, index = index, doc_type = doc_type)

if __name__ == '__main__':
    path = sys.argv[1]
    load_dir(path, '.xml', paper_xml_to_doc, collection = PAPER_EN_COLLECTION, index = PAPER_EN_INDEX, doc_type = PAPER_EN_TYPE)

