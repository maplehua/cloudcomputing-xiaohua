# -*- coding: utf-8 -*-
from pyes import CustomScoreQuery, BoolQuery, TermQuery, TextQuery, HighLighter, Search
from app import es_conn, mongo_conn
from app.models.ScholarMeta import ScholarMeta
from app.models.PaperMeta import PaperMeta
from app.models.Affiliation import Affiliation
from translate import trans
from config import *

class AcademiSearch():
    def __init__(self, theme = 'scholar', keyword = 'name', offset = 0, page = 1):
        self.theme = theme
        self.keyword = keyword
        self.offset = offset
        self.page = page

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
        name =  self.keyword
        name = name.encode("utf-8")
        scholars = scholar_get_scholars(name)
        return scholars

    def _scholar_single_search(self, ccf_rank = None):
        user_id = self.offset
        scholar = scholar_fetch_meta(user_id, self.keyword)
        papers = ScholarMeta.get_papers(sch_name = self.keyword, ccf_rank = ccf_rank, page = self.page)
        stat = ScholarMeta.stat_papers(sch_name = self.keyword)
        return dict(scholar = scholar,
                papers = papers,
                stat = stat)

    def _scholar_single_ccf_a_search(self):
        return self._scholar_single_search('A')
    def _scholar_single_ccf_b_search(self):
        return self._scholar_single_search('B')
    def _scholar_single_ccf_c_search(self):
        return self._scholar_single_search('C')
    def _scholar_single_ccf_u_search(self):
        return self._scholar_single_search('unknow')

    def _affiliation_search(self, ccf_rank = None):
        affi = Affiliation.get_affiliation(self.keyword)
        papers =  affi.get_papers(ccf_rank = ccf_rank, page = self.page)
        count_paper_by_year= affi.get_year_papers()
        return dict(affiliation = affi,
                papers = papers,
                stat = affi.stat_papers(),
                count_paper_by_year=count_paper_by_year)

    def _affiliation_ccf_a_search(self):
        return self._affiliation_search('A')
    def _affiliation_ccf_b_search(self):
        return self._affiliation_search('B')
    def _affiliation_ccf_c_search(self):
        return self._affiliation_search('C')
    def _affiliation_ccf_u_search(self):
        return self._affiliation_search('unknow')

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
    highlight = HighLighter(pre_tags = ['<strong class="text-danger">'], post_tags = ['</strong>'])
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

# scholar serach pipeline
def scholar_get_scholars(keyword):
    scholars =  ScholarMeta.objects(name_low_case = keyword.lower(), ban = 0)
    if scholars.count()== 0:
        if PaperMeta.objects(authors_low_case = keyword.lower()).count() > 0:
            scholar = ScholarMeta(name = keyword.title(), scholar_id = '0')
            return [scholar]
    return scholars

def scholar_fetch_meta(scholar_id, name):
    if scholar_id == '0':
        scholar = ScholarMeta(name = name.title())
    else:
        scholar = ScholarMeta.objects(scholar_id = scholar_id).first_or_404()
    return scholar
