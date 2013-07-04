# -*- coding: utf-8 -*-
import json
import pprint
from pyes import ES, CustomScoreQuery, BoolQuery, TermQuery, TextQuery, HighLighter, Search
from app import es_conn, mongo_conn
from translate import trans
from config import *

class AcademiSearch():
    def __init__(self, theme, keyword, offset):
        self.theme = theme
        self.keyword = keyword
        self.offset = offset

    def result(self):
        search_func = getattr(self, '_%s_search' % self.theme)
        return search_func()

    def _paper_search(self):
        keywords = expand(self.keyword)
        stat = paper_es_stat(keywords)
        result_list = paper_es_search(keywords, self.offset, RESULT_SIZE)
        total = result_list.total
        papers = []
        for result in result_list:
            meta_doc = paper_fetch_meta(result.uuid)
            papers.append(paper_rebuild(result, meta_doc))
        return dict(total = total,
                papers = papers,
                stat = stat)

# paper serach pipe line
def expand(keyword):
    trans_keyword = trans(keyword)
    return [keyword, trans_keyword]

def paper_es_stat(keywords):
    qlist = []
    for k in keywords:
        qlist.append(TextQuery(field = 'title', text = k, type = 'phrase'))
        qlist.append(TextQuery(field = 'body', text = k, type = 'phrase'))
        qlist.append(TextQuery(field = 'title', text = k, operator='and'))
        qlist.append(TextQuery(field = 'body', text = k, operator = 'and'))

    fields = ['title', 'uuid']
    query = BoolQuery(should = qlist, disable_coord = True)
    highlight = HighLighter()
    highlight.add_field(name = 'body')
    highlight.add_field(name = 'title')

    s = Search(query = query, fields = fields, highlight = highlight)

    results =  es_conn.search(s, indices = PAPER_INDEX)
    stat_body = 0
    stat_title = 0
    for result in results:
        if 'title' in result._meta.highlight:
            stat_title += 1
        if 'body' in result._meta.highlight:
            stat_body += 1
    return dict(title = stat_title,
            body = stat_body)


def paper_es_search(keywords, start, size):
    if isinstance(start, str) or isinstance(start, unicode):
        start = int(start)
    qlist = []
    for k in keywords:
        qlist.append(TextQuery(field = 'title', text = k, type = 'phrase'))
        qlist.append(TextQuery(field = 'body', text = k, type = 'phrase'))
        qlist.append(TextQuery(field = 'title', text = k, operator='and'))
        qlist.append(TextQuery(field = 'body', text = k, operator = 'and'))

    fields = ['title', 'uuid']
    query = BoolQuery(should = qlist, disable_coord = True)
    highlight = HighLighter(pre_tags = ['<strong class="text-error">'], post_tags = ['</strong>'])
    highlight.add_field(name = 'body', fragment_size = 200, number_of_fragments = 3)
    highlight.add_field(name = 'title', fragment_size = 500, number_of_fragments = 1)

    s = Search(query = query, fields = fields, highlight = highlight, start=start, size=size, explain = EXPLAIN)

    results =  es_conn.search(s, indices = PAPER_INDEX)
    return results

def paper_fetch_meta(uuid):
    return mongo_conn[PAPER_COLLECTION].find_one(spec_or_id = {"uuid": uuid}, fields = ['title', 'authors', 'publication', 'year'])

def paper_rebuild(es_result, mongo_doc):
    uuid = es_result.uuid
    score = es_result._meta.score
    highlight = []
    if 'body' in es_result._meta.highlight:
        highlight = es_result._meta.highlight['body']

    title = mongo_doc['title']
    authors = mongo_doc['authors']
    publication = mongo_doc['publication']
    year = mongo_doc['year']

    new_result =  dict(uuid = uuid, score = score, highlight = highlight, title = title, authors = authors, publication = publication, year = year)

    if EXPLAIN:
        new_result['explain'] = es_result._meta.explanation

    return new_result




