#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import re
import argparse
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

def paper_html_to_doc(infile):
    paper = BeautifulSoup(open(infile))

    uuid = unicode(uuid1())

    title = paper.find('meta', attrs={'name':'DC.Title'})['content']
    publication = '中国科学'
    year = paper.find('meta', attrs={'name':'DC.Date'})['content'].strip()
    body = paper.find('meta', attrs={'name':'DC.Description'})['content'].strip()
    authors = []
    author_list = paper.find('meta', attrs={'name':'citation_authors'})['content']
    authors_o = re.split(r",| *|;", author_list)
    for a in authors_o:
        authors.append(a.strip())


    mongo_doc = dict(uuid = uuid, title = title, authors = authors, publication = publication, year = year, body = body)
    es_doc = dict(uuid = uuid, title = title, body = body)
    #print title
    #print publication
    #print year
    #print authors
    #print body
    #return (1,1)
    return (mongo_doc, es_doc)


def paper_xml_to_doc(infile):
    paper = BeautifulSoup(open(infile))

    uuid = unicode(uuid1())

    title = paper.title.get_text().strip()
    publication = paper.conference.get_text().strip()
    year = paper.year.get_text().strip()
    body = paper.body.get_text()

    authors = []
    author_list = paper.find_all('author')
    for a in author_list:
        authors.append(a.get_text().strip())

    mongo_doc = dict(uuid = uuid, title = title, authors = authors, publication = publication, year = year, body = body)
    es_doc = dict(uuid = uuid, title = title, body = body)
    return (mongo_doc, es_doc)

def import_mongo(doc, collection):
    return mongo_conn[collection].insert(doc)

def import_es(doc, index, doc_type):
    return es_conn.index(doc = doc, index = index, doc_type = doc_type)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Academi Data Import Utility')
    parser.add_argument('-t', dest='data_type', help='data type')
    parser.add_argument('path', help='Data path')
    args = parser.parse_args()
    if args.data_type == 'paper':
        print 'import paper', args.path
        load_dir(args.path, '.xml2', paper_xml_to_doc, collection = PAPER_COLLECTION, index = PAPER_INDEX, doc_type = PAPER_TYPE)
    elif args.data_type == 'paper_en':
        print 'paper_en', args.path
        load_dir(args.path, '.xml', paper_xml_to_doc, collection = PAPER_EN_COLLECTION, index = PAPER_EN_INDEX, doc_type = PAPER_EN_TYPE)
    elif args.data_type == 'paper_cn':
        print 'paper_cn', args.path
        load_dir(args.path, '.html', paper_html_to_doc, collection = PAPER_COLLECTION, index = PAPER_INDEX, doc_type = PAPER_TYPE)



#print(args.accumulate(args.integers))
