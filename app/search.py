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
        keyword = self.keyword
        scholars = scholar_get_scholars(keyword)
        papers = []
        total = len(scholars)
        return dict(total = total,
                scholars = scholars)

    def _scholar_single_search(self):
        user_id = self.offset
        name = self.keyword
        scholar = scholar_fetch_meta(user_id, name)
        papers = scholar_get_papers(name)
        stat = scholar_stat_papers(name)
        return dict(scholar = scholar,
                papers = papers,
                stat = stat)

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

# scholar serach pipeline
def scholar_get_scholars(keyword):
    scholars=[]
    sch_cur = mongo_conn.Microsoft_AS.AuthorInfo.find({u"NameLowCase": keyword.lower(), 'invisible': 0})
    if sch_cur.count() > 0:
        for sch in sch_cur:
            scholars.append(sch)
    elif mongo_conn.dblp.dblp_papers_all.find({"authors_low_case": keyword.lower()}).count() > 0:
        scholar = {'Name': keyword.title(), 'user_id': '0'}
        scholars.append(scholar)
    return scholars

def scholar_fetch_meta(user_id, name):
    '''
    return a scholar's info by id
    '''
    if user_id == '0':
        scholar = {'Name': name.title()}
    else:
        scholar = mongo_conn['Microsoft_AS']['AuthorInfo'].find_one(spec_or_id = {'user_id': user_id}, fields = ['Name', 'NativeName', 'Photo', 'Affiliation', 'Homepage', 'Email'])
    return scholar

def scholar_get_papers(name):
    sort_field = [('year', -1)]
    papers = mongo_conn.dblp.dblp_papers_all.find({'authors_low_case': name.lower()}).sort(sort_field)
    paper_all = []
    for p in papers:
        paper_all.append(p)

    sort_field = [('ccf_rank', 1), ('year', -1)]
    papers = mongo_conn.dblp.dblp_papers_all.find({'authors_low_case': name.lower(), 'ccf_rank': 'A'}).sort(sort_field)
    paper_rank_a = []
    for p in papers:
        paper_rank_a.append(p)

    papers = mongo_conn.dblp.dblp_papers_all.find({'authors_low_case': name.lower(), 'ccf_rank': 'B'}).sort(sort_field)
    paper_rank_b = []
    for p in papers:
        paper_rank_b.append(p)

    papers = mongo_conn.dblp.dblp_papers_all.find({'authors_low_case': name.lower(), 'ccf_rank': 'C'}).sort(sort_field)
    paper_rank_c = []
    for p in papers:
        paper_rank_c.append(p)

    papers = mongo_conn.dblp.dblp_papers_all.find({'authors_low_case': name.lower(), 'ccf_rank': 'unknow'}).sort(sort_field)
    paper_rank_unknow = []
    for p in papers:
        paper_rank_unknow.append(p)

    return {'paper_all': paper_all, 'paper_rank_a': paper_rank_a, 'paper_rank_b': paper_rank_b, 'paper_rank_c': paper_rank_c, 'paper_rank_unknow': paper_rank_unknow}

def scholar_stat_papers(name):
    count_all = mongo_conn.dblp.dblp_papers_all.find({'authors_low_case': name.lower()}).count()
    count_rank_a = mongo_conn.dblp.dblp_papers_all.find({'authors_low_case': name.lower(), 'ccf_rank': 'A'}).count()
    count_rank_b = mongo_conn.dblp.dblp_papers_all.find({'authors_low_case': name.lower(), 'ccf_rank': 'B'}).count()
    count_rank_c = mongo_conn.dblp.dblp_papers_all.find({'authors_low_case': name.lower(), 'ccf_rank': 'C'}).count()
    count_rank_unknow = count_all - count_rank_a - count_rank_b - count_rank_c
    prop_rank_a = count_rank_a * 100 / count_all
    prop_rank_b = count_rank_b * 100 / count_all
    prop_rank_c = count_rank_c * 100 / count_all
    prop_rank_unknow = (100 - prop_rank_a - prop_rank_b - prop_rank_c)
    print prop_rank_unknow
    return {'count_all': count_all,
            'count_rank_a': count_rank_a,
            'count_rank_b': count_rank_b,
            'count_rank_c': count_rank_c,
            'count_rank_unknow': count_rank_unknow,
            'prop_rank_a': prop_rank_a,
            'prop_rank_b': prop_rank_b,
            'prop_rank_c': prop_rank_c,
            'prop_rank_unknow': prop_rank_unknow}
