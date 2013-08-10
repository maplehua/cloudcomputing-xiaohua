#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, json, re
from pprint import pprint
from pymongo import MongoClient
from rank_list import jour_list, conf_list

from config import *

mongo_conn = MongoClient(host = MONGODB_HOST, port = MONGODB_PORT)
def rank_journal():
    for journal in jour_list:
        jour_name = journal['dblp_name']
        ccf_rank = journal['ccf']
        mongo_conn['dblp']['dblp_papers_all'].update({'journal': jour_name}, {'$set': {'ccf_rank': ccf_rank.upper()}}, multi = True)
        print 'rank %s to journal: %s' % (ccf_rank, jour_name)

def rank_conference():
    for conference in conf_list:
        conf_name = conference['dblp_name']
        ccf_rank = conference['ccf']
        mongo_conn['dblp']['dblp_papers_all'].update({'booktitle': conf_name}, {'$set': {'ccf_rank': ccf_rank.upper()}}, multi = True)
        for i in xrange(100):
            mongo_conn['dblp']['dblp_papers_all'].update({'booktitle': '%s (%d)' % (conf_name, i)}, {'$set': {'ccf_rank': ccf_rank.upper()}}, multi = True)
        print 'rank %s to conference: %s' % (ccf_rank, conf_name)

if __name__ == '__main__':
    rank_journal()
    rank_conference()
