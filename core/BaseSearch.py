#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from pprint import pprint
from pyes import ES, CustomScoreQuery, BoolQuery, TermQuery, TextQuery, HighLighter, Search
from pymongo import MongoClient

from settings import ES_SETTING, RESULT_SIZE, DEBUG
from settings import ES_META
from settings import MONGO_DB, MONGO_SERVER, DICTIONARY_COLLECTION

ES_SERVER = ES_SETTING['server']
pre_tag = ES_SETTING['pre_tag']
post_tag = ES_SETTING['post_tag']

paper_index = ES_META['paper']['index']
paper_type = ES_META['paper']['type']
patent_index = ES_META['patent']['index']
patent_type = ES_META['patent']['type']

class ESSearch(object):
    def __init__(self, index, doc_type):
        self.conn = ES(ES_SERVER)
        self.index = index
        self.doc_type = doc_type

class MongoSearch(object):
    def __init__(self, collection):
        self.conn = MongoClient(MONGO_SERVER)[MONGO_DB][collection]

    def _get(self, query):
        return self.conn.find_one(query)

    def _gets(self, query):
        return self.conn.find(query)

class PaperSearch(ESSearch):
    def __init__(self):
        ESSearch.__init__(self, paper_index, paper_type)
        self.search_field = ES_META['paper']['search']
        self.result_field = ES_META['paper']['result']

    def get_results(self, keywords, pos):
        results =  self._get_results(keywords, pos, RESULT_SIZE, self.search_field, self.result_field)
        papers = []
        for r in results:
            paper = self._rebuild(r)
            papers.append(paper)
        return papers

    def append_query(self, qlist, q, weight = None):
        if weight:
            qlist.append(CustomScoreQuery(query = q, script = "_score * %s" % weight))
        else:
            qlist.append(q)

    def _get_results(self, keywords, start, size, search_fields = None, rfields = None):
        query_list = []
        for k in keywords:
            q = TextQuery(field = 'title', text = k, type = 'phrase')
            self.append_query(query_list, q, 100)
            q = TextQuery(field = 'content', text = k, type = 'phrase')
            self.append_query(query_list, q, 200)

            q = TextQuery(field = 'title', text = k, operator='and')
            self.append_query(query_list, q)
            q = TextQuery(field = 'content', text = k, operator = 'and')
            self.append_query(query_list, q)


        q = BoolQuery(should = query_list, disable_coord = True)

        h = HighLighter(pre_tags = [pre_tag], post_tags = [post_tag])
        for f in search_fields:
            h.add_field(name = f, fragment_size = 200, number_of_fragments = 3)
        s = Search(query = q, fields = rfields, highlight = h, start=start, size=size, explain = True)
        if DEBUG:
            print '=== Query DL ==='
            pprint(json.loads(s.to_search_json()))
            print s.to_search_json()
            print '================'

        results =  self.conn.search(s, indices = self.index)
        return results

    def _rebuild(self, result):
        paper = dict(title = result.title,
                author = result.author,
                source = result.source,
                year = result.year,
                url = result.url,
                content = result._meta.highlight.content)
        if DEBUG:
            paper['score'] = result._meta.score
            print '=== %s ===' % paper['title']
            #pprint(result._meta.explanation)
            print '========='
        return paper

class DictionarySearch(MongoSearch):
    def __init__(self):
        MongoSearch.__init__(self, DICTIONARY_COLLECTION)

    def translate(self, keyword):
        results = self._gets({'from':keyword})
        trans_list = []
        for item in results:
            trans_list.append(item['to'])
        return trans_list
