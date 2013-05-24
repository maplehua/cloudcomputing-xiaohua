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

def load_dir(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if '.xml' == f[-4:]:
                print os.path.join(root, f)
                c = read_xml(os.path.join(root, f))
                print to_mongo(c)


def read_xml(infile):
    paper = BeautifulSoup(open(infile))

    title = paper.title.get_text()
    source = paper.conference.get_text()
    year = paper.year.get_text()
    content = paper.body.get_text()

    authors = ""
    author_list = paper.find_all('author')
    for a in author_list:
        authors += a.get_text() + ', '

    author = authors[:-2]

    url = 'http://scholar.google.com/scholar?q=%s' % quote(title.encode("utf-8"))

    return dict(title = title, author = author, source = source, year = year, content = content, url = url)

def to_mongo(json):
    conn = MongoClient('10.77.20.50')[MONGO_DB]['paper']
    identify = conn.insert(json)
    return identify

if __name__ == '__main__':
    path = sys.argv[1]
    load_dir(path)

