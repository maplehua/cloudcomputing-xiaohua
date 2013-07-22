#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import codecs
from uuid import uuid1
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pyes import ES

from config import *

fin = open('/Users/guxiangnan/Data/index', 'r')
count = 0
mydic = {}
while True:
    title = fin.readline().strip()
    if not title:
        break
    meta = fin.readline()
    author = fin.readline()
    pub = fin.readline()
    year = fin.readline().strip()
    path1 = fin.readline().strip()
    path2 = fin.readline()
    count += 1
    path = path1.split('\\')
    key =  'SIGMOD\\SIGMOD%s\\%s' % (path[2], path[3])
    value = title
    mydic[key] = value

def load_dir(path, file_type,parse_func, collection, index, doc_type):
    for root, dirs, files in os.walk(path):
        for f in files:
            if file_type == f[-len(file_type):]:
                print os.path.join(root, f)
                parse_func(os.path.join(root, f), os.path.join(root, '%s2' % f))

def paper_xml_to_doc(infile, outfile):
    paper = BeautifulSoup(open(infile))
    uuid = unicode(uuid1())
    title = paper.title
    pdfpath = paper.pdfpath.get_text().strip()
    newtitle = mydic[pdfpath]
    if newtitle:
        paper.title.string = newtitle
    else:
        print '\tN%s' % paper.title.get_text()

    codecs.open(outfile,'w','utf-8').write(paper.paper.prettify(formatter="xml"))

if __name__ == '__main__':
    path = sys.argv[1]
    load_dir(path, '.xml', paper_xml_to_doc, collection = PAPER_COLLECTION, index = PAPER_INDEX, doc_type = PAPER_TYPE)

