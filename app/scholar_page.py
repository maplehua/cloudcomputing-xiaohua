# -*- coding: utf-8 -*-
from app import mongo_conn
def get_scholar_by_id(scholar_id):
    scholar=mongo_conn.Microsoft_AS.AuthorInfo.find_one({u"ID":scholar_id})
    if scholar:
        return scholar
    else:
        return None

def get_papers_by_id(scholar_id):
    scholar=mongo_conn.Microsoft_AS.AuthorInfo.find_one({u"ID":scholar_id})
    mycursor=mongo_conn.dblp.dblp_papers_all.find({"authors":scholar[u"Name"]})
    papers=[]
    for p in mycursor:
        papers.append(p)
    return papers
