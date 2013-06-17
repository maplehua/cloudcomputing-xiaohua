#!/usr/bin/python
# -*- coding: utf-8 -*-
import settings
import os, sys
sys.path.append(settings.LIB_PATH)

import json

from urllib import quote
from bs4 import BeautifulSoup
from pymongo import MongoClient
from settings import MONGO_DB
from pprint import pprint

def load_dir(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if '.html' == f[-5:]:
                print os.path.join(root, f)
                c = read_xml(os.path.join(root, f))
                print to_mongo(c)
                #pprint(c)


def read_xml(infile):
    paper = BeautifulSoup(open(infile), 'lxml')

    title = paper.find('meta', attrs = {'name':'DC.Title'})['content']
    source = 'SSI'
    year = paper.find('meta', attrs = {'name':'DC.Date'})['content']
    content = paper.find('meta', attrs={'name':'DC.Description', 'xml:lang':'cn'})['content']
    author = paper.find('meta', attrs={'name':'citation_authors', 'xml:lang':'cn'})['content']
    url = paper.find('meta', attrs = {'name':'HW.ad-path'})['content']

    return dict(title = title, author = author, source = source, year = year, content = content, url = url)

def to_mongo(json):
    conn = MongoClient('10.77.20.50')[MONGO_DB]['paper']
    identify = conn.insert(json)
    return identify

if __name__ == '__main__':
    path = sys.argv[1]
    load_dir(path)

