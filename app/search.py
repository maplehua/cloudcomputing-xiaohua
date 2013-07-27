# -*- coding: utf-8 -*-
from pyes import CustomScoreQuery, BoolQuery, TermQuery, TextQuery, HighLighter, Search
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
        keywords = paper_keyword_expand(self.keyword)
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

    def _paper_en_search(self):
        keywords = [self.keyword]
        stat = paper_en_es_stat(keywords)
        result_list = paper_en_es_search(keywords, self.offset, RESULT_SIZE)
        total = result_list.total
        papers = []
        for result in result_list:
            meta_doc = paper_en_fetch_meta(result.uuid)
            papers.append(paper_en_rebuild(result, meta_doc))
        return dict(total = total,
                papers = papers,
                stat = stat)

    def _paper_title_search(self):
        '''
        search paper in title, statistic all fields
        '''
        keywords = paper_keyword_expand(self.keyword)
        stat = paper_es_stat(keywords)
        result_list = paper_title_es_search(keywords, self.offset, RESULT_SIZE)
        total = result_list.total
        papers = []
        for result in result_list:
            meta_doc = paper_fetch_meta(result.uuid)
            papers.append(paper_rebuild(result, meta_doc))
        return dict(total = total,
                papers = papers,
                stat = stat)

    def _paper_body_search(self):
        '''
        search paper in body, statistic all fields
        '''
        keywords = paper_keyword_expand(self.keyword)
        stat = paper_es_stat(keywords)
        result_list = paper_body_es_search(keywords, self.offset, RESULT_SIZE)
        total = result_list.total
        papers = []
        for result in result_list:
            meta_doc = paper_fetch_meta(result.uuid)
            papers.append(paper_rebuild(result, meta_doc))
        return dict(total = total,
                papers = papers,
                stat = stat)

    def _scholar_search(self):
        keyword=self.keyword
        scholar=get_scholar(keyword)
        papers=get_papers(keyword)
        #stat = paper_en_es_stat(keywords)
        #result_list = paper_en_es_search(keywords, self.offset, RESULT_SIZE)
        #total = result_list.total
        #papers = []
        #for result in result_list:
        #    meta_doc = paper_en_fetch_meta(result.uuid)
        #    papers.append(paper_en_rebuild(result, meta_doc))
        return dict(scholar=scholar,
                papers = papers)


### paper serach pipe line
def paper_keyword_expand(keyword):
    '''
    expand keyword from single language into bilingual
    '''
    trans_keyword = trans(keyword)
    return [keyword, trans_keyword]

def paper_es_stat(keywords):
    '''
    statistic search result
    return:
        number of hit in title
        number of hit in body
    '''
    qlist = []
    for k in keywords:
        qlist.append(TextQuery(field = 'title', text = k, type = 'phrase'))
        qlist.append(TextQuery(field = 'title', text = k, operator='and'))
    query = BoolQuery(should = qlist, disable_coord = True)
    s = Search(query = query)
    results =  es_conn.search(s, indices = PAPER_INDEX)
    stat_title = results.total
    qlist = []
    for k in keywords:
        qlist.append(TextQuery(field = 'body', text = k, type = 'phrase'))
        qlist.append(TextQuery(field = 'body', text = k, operator = 'and'))
    query = BoolQuery(should = qlist, disable_coord = True)
    s = Search(query = query)
    results =  es_conn.search(s, indices = PAPER_INDEX)
    stat_body = results.total
    qlist = []
    for k in keywords:
        qlist.append(TextQuery(field = 'title', text = k, type = 'phrase'))
        qlist.append(TextQuery(field = 'title', text = k, operator='and'))
        qlist.append(TextQuery(field = 'body', text = k, type = 'phrase'))
        qlist.append(TextQuery(field = 'body', text = k, operator='and'))
    query = BoolQuery(should = qlist, disable_coord = True)
    s = Search(query = query)
    results =  es_conn.search(s, indices = PAPER_INDEX)
    stat_all = results.total
    qlist = []
    return dict(title = stat_title,
            body = stat_body,
            all = stat_all,
            first_paper = {'title':'TITLE','year':'2013'},
            contribution = 'CONTRIBUTION')

def paper_es_search(keywords, start, size):
    '''
    search papers which hit keyword in title and body
    '''
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

def paper_title_es_search(keywords, start, size):
    '''
    search papers which hit keyword in title
    '''
    if isinstance(start, str) or isinstance(start, unicode):
        start = int(start)
    qlist = []
    for k in keywords:
        qlist.append(TextQuery(field = 'title', text = k, type = 'phrase'))
        qlist.append(TextQuery(field = 'title', text = k, operator='and'))
    fields = ['title', 'uuid']
    query = BoolQuery(should = qlist, disable_coord = True)
    highlight = HighLighter(pre_tags = ['<strong class="text-error">'], post_tags = ['</strong>'])
    highlight.add_field(name = 'title', fragment_size = 500, number_of_fragments = 1)
    s = Search(query = query, fields = fields, highlight = highlight, start=start, size=size, explain = EXPLAIN)
    results =  es_conn.search(s, indices = PAPER_INDEX)
    return results

def paper_body_es_search(keywords, start, size):
    '''
    search papers which hit keyword in body
    '''
    if isinstance(start, str) or isinstance(start, unicode):
        start = int(start)
    qlist = []
    for k in keywords:
        qlist.append(TextQuery(field = 'body', text = k, type = 'phrase'))
        qlist.append(TextQuery(field = 'body', text = k, operator='and'))
    fields = ['title', 'uuid']
    query = BoolQuery(should = qlist, disable_coord = True)
    highlight = HighLighter(pre_tags = ['<strong class="text-error">'], post_tags = ['</strong>'])
    highlight.add_field(name = 'body', fragment_size = 500, number_of_fragments = 1)
    s = Search(query = query, fields = fields, highlight = highlight, start=start, size=size, explain = EXPLAIN)
    results =  es_conn.search(s, indices = PAPER_INDEX)
    return results

def paper_fetch_meta(uuid):
    return mongo_conn[PAPER_DB][PAPER_COLLECTION].find_one(spec_or_id = {"uuid": uuid}, fields = ['title', 'authors', 'publication', 'year'])

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

### paper_en_serach pipe line
def paper_en_es_stat(keywords):
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
    results =  es_conn.search(s, indices = PAPER_EN_INDEX)
    stat_body = 0
    stat_title = 0
    for result in results:
        if 'title' in result._meta.highlight:
            stat_title += 1
        if 'body' in result._meta.highlight:
            stat_body += 1
    return dict(title = stat_title,
            body = stat_body)


def paper_en_es_search(keywords, start, size):
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
    results =  es_conn.search(s, indices = PAPER_EN_INDEX)
    return results
def paper_en_fetch_meta(uuid):
    return mongo_conn[PAPER_DB][PAPER_EN_COLLECTION].find_one(spec_or_id = {"uuid": uuid}, fields = ['title', 'authors', 'publication', 'year'])

def paper_en_rebuild(es_result, mongo_doc):
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

def get_scholar(keyword):
    scholar=mongo_conn.Microsoft_AS.AuthorInfo.find_one({u"Name":keyword})
    #default_ph=u"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBAQFBAYFBQYJBgUGCQsIBgYICwwKCgsKCgwQDAwMDAwMEAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/2wBDAQcHBw0MDRgQEBgUDg4OFBQODg4OFBEMDAwMDBERDAwMDAwMEQwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCABgAGADAREAAhEBAxEB/8QAGwAAAgMBAQEAAAAAAAAAAAAAAAQDBQYBAgf/xAA5EAACAQMCAggCCAUFAAAAAAABAgMABBEFIRIxBhMUIjJBUXFCUhUzQ2FicoGCI6GisbJEU5HS8P/EABkBAQEBAQEBAAAAAAAAAAAAAAABAgMEBf/EABgRAQEBAQEAAAAAAAAAAAAAAAABEQIx/9oADAMBAAIRAxEAPwD7jX0XgFAUBQFAUBQFBwugOCwBPIE0HJJYo/G4X3OKDqsrDKkEHkRuKDtAUCcusaXFL1Ul1GrjYji5H7/Sria8XGvaRBjjuUYncCPvn+nNMNM2l7a3cfWW0qypyJHl7g7ioqagKAoFb26ZMRRfWt5/KPWqUkLePHeHEx5seZojqwRD4c++/wDeg6jtbN1kfg+0j8iPUUFojK6hlOVYZB96iqTXdTkMn0daNwykZuZR8CHyH4mqyM2q6O1t40CLGvD94Bz71pHqOCGPPVoqZ58IAoI2MtnN2207sqbyx/DIvmDUGqtbmO5t47iM9yRQw/WstiO8tJZDHFPG8i+JFZSw9wDQQalq+m6bCZLy5ig2JRZHVS2PQE5NXEtV2n31pfRm5t7iO54zl3jYNg+hxyqpDdRRQcoJ9Nk/htCecR2/KdxQjOWcZWISOxeWXvyueZZt60ynqAoOOyqpZyFRQSzHYADnmgyLXl7rMbWazMmgQyN1SLlWn3+I8+rU8h/5dYzobo9o5AAtgpHJlLKwPuDmqmPcWi6fHIZHjM8p+0nJkbA5eLNBySwltZ+3aSwtb1PJdo5R8jry3oNh0f1uHV7ETqvVXEZ6u6tz4o5BzHt8tYsdJdWdRRQdtM9u2/2zxf8ANBUKAFAHIDAqsigKDNdIb17+7+hbZsQqA+oyrzC8xED6t8VajNSxxpGixooVEACqOQAqo9UBQFBDpVx9HdKYW5W+qJ1Evp1ybxt7t4KlWet1WHR5d1RSx5CgasIGRWlkGJJPL0UchRYzNq0kebSccFzB3XU+YHJh6itMGKgKDH6IeNb2Y7tLdzMX9RxYH6VthZUC93qFlaAdolEZO4Xckj2GTQeLXVdPum4IJlZ/lOVJ9gwFA3QJaxbPPYSdWcTxYlgYcw8feGP7UG00bUF1HSrW9X7eNWYejcmH6NmsV0lMsVWaJpAeqU5bG+/lmoq2ByMjlUVm9dkW51WKBFCm0AeWX4jxbhB+GtRmo6IV1ZZ20u7W3OJzDII8c+LhOMVYlZ3RDAdJtTAAE6sZA+b4v6s1pk9QJXmj2N5cLPcKXZV4AvEQMAk+WD50Gb1q1t7C/i7ExVwA3ADxFWB2++qNguSBnY+YqCO6mWG2lmbZY0Zj+gzQX/Qy2e26L6fE4wxj6zB9JGLj/KsX1058XDKGUqeRGKipIb2aFQkqcaKMB154HqKGqOG3SIs2WeRzmSRzlmP3mtMpKgKDIwoun6xeac3cjlbtNmPIq/jVfytW2FhQJaxHJJplwkalnK7Ku5O49KCt0DRIViS6uYnFwGPCkmwGDseHA/nQX9Aj2WXXNQGlQZ7JEVfUpxyVQciMH52qWrJr6AiKiKiAKqgBVGwAHIVh0eqAoKmqyKAoENa0qz1C1xcN1Tw5eK5U4aMj4gfT1qypYodFu57mzLTEOUkaNZlGFkVTgOAfWtMpdSS6exlS1JW4I7hBweYzg+W1BFo0V/FZ8N6SZuIkcTcRC+WTk0EuqXfY9PnuB4o17v5jsv8AM0Gp6NaQml6TDBjM7jrbpzzaV92J/wAaxa6SYtaiigKCpqsigKDNdLNRtp4o9JglElxPNGs8UeSViBy3ER4eXnWozUqIkaKiKFRRhVGwAFVHqgKCOeCG4haGZQ8TjDKfOgb6E3hhuL/R5ZiwgZZLNJGy3VyLllXO5CEVnprmtbWWxQFBU1WVXqnSPT7B+oBNzeHw2sI4n/d5L+tXEtU0za7qee2T9htW/wBJbnvkejyf9a1jKe0sLSzTgt4ggPiPNj7k7mgYoCgKAoFbzTbW74WkUrKn1cyHhkX2YUEttrHSfTcAuuq2o5pJ3JwPufk37qmLOq0Gk9K9I1JxCsht7zk1pOOCTPoM7N+2s2NzrVzUVi+kGp3ZuY9KsH6qeVesuLgc4os47v42rcjnaWstOtbKPhgTDHd5Du7H1ZqqGaAoCgKAoCgKAoF7ywtLxOGeMNjwvyZT+FhuKCz6H6jdi5utHu5mnNsqy2sz7uYW2IY+fA21Zsb5r//Z"
    if scholar:
        #if scholar[u"Photo"]==u"AAA":
        #    scholar[u"Photo"]=default_ph
        #scholar[u"Photo"]="data:image/gif;base64,"+scholar[u"Photo"]
        return scholar
    else:
        return None

def get_papers(keyword):
    mycursor=mongo_conn.dblp.dblp_papers_all.find({"authors":keyword})
    papers=[]
    for p in mycursor:
        papers.append(p)
    return papers
