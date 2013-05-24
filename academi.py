#!/usr/bin/python
# -*- coding: utf-8 -*-
import settings
from settings import DEBUG
if settings.LIB_PATH:
    import sys
    sys.path.append(settings.LIB_PATH)

from bottle import Bottle, request, route, run, static_file, error
from bottle import PluginError, response
from bottle import jinja2_view as view
from bottle import jinja2_template as template
from models import jsonlist

from core.BaseSearch import PaperSearch, DictionarySearch
from core.Dictionary import expand_keyword

from utils.pagination import gen_pos
from utils.about_mongo import about_readmongo
from settings import RESULT_SIZE
from bottle_mongo import MongoPlugin


app = Bottle()
plugin = MongoPlugin(uri="10.77.20.50:27017", db="academi", json_mongo=True)
app.install(plugin)
@app.route('/show/:item')
def show(item, mongodb):
    doc = mongodb['about_weibo'].find({item:"item"})
    return doc

@app.route('/')
@app.route('/paper/')
@view('homepage_paper')
def paper_index():
    return dict(theme = 'paper')

@app.route('/scholar/')
@view('homepage_scholar')
def scholar_index():
    scholar_actived=True
    return dict(scholar_actived = scholar_actived, theme = 'scholar')

@app.route('/patent/')
@view('homepage_patent')
def patent_index():
    patent_actived=True
    return dict(patent_actived = patent_actived, theme = 'patent')

@app.route('/weibo/')
@view('homepage_weibo')
def weibo_index():
    weibo_actived=True
    return dict(weibo_actived = weibo_actived, theme = 'weibo')

@app.route('/blog/')
@view('homepage_blog')
def blog_index():
    blog_actived=True
    return dict(blog_actived = blog_actived, theme = 'blog')

@app.route('/about/')
@view('about')
def about():
    keyword = request.forms.get('keyword')
    pages = about_readmongo("about_page")
    papers = about_readmongo("about_paper")
    weibos = about_readmongo("about_weibo")
    query = dict(keyword = keyword, theme = 'about')
    return dict(pages = pages, papers=papers, weibos=weibos, page_actived = True, query = query)

def deco_get_keywords(func):
    def _deco_func(keyword = None, pos = 0):
        if not keyword:
            keyword = request.forms.get('keyword')
            pos = int(request.forms.get('pos'))
        ret = func(keyword, pos)
        return ret
    return _deco_func

# [Search]
@app.get('/paper/search/<keyword>/<pos:int>')
@app.post('/paper/search')
@view('result_paper')
@deco_get_keywords
def search_paper(keyword, pos):
    (pre, cur, post) = gen_pos(pos)

    if settings.KEYWORD_EXPAND:
        keywords = expand_keyword(keyword)
    else:
        keywords = [keyword]

    s = PaperSearch()
    results = s.get_results(keywords, pos)
    meta = dict(keyword = keyword, theme = 'paper', pre = pre, cur = cur, post = post)
    return dict(papers = results, query = meta)

@app.get('/patent/search/<keyword>/<pos:int>')
@app.post('/patent/search')
@view('result_patent')
@deco_get_keywords
def search_patent(keyword, pos):
    (pre, cur, post) = gen_pos(pos)
    s = PatentSearch()
    results = s.get_results(keyword, pos)
    query = dict(keyword = keyword, theme = 'patent', pre = pre, cur = cur, post = post)
    return dict(patents = results, patent_actived = True, query = query)

@app.get('/scholar/search/<keyword>/<pos:int>')
@app.post('/scholar/search')
@view('result_scholar')
@deco_get_keywords
def get_scholar_result(keyword, pos):
    (pre, cur, post) = gen_pos(pos)
    s = ScholarSearch()
    results = s.get_results(keyword, pos)
    query = dict(keyword = keyword, theme = 'scholar', pre = pre, cur = cur, post = post)
    return dict(scholars = results, scholar_actived = True, query = query)

@app.route('/weibo/search/<keyword>/<pos:int>')
@app.post('/weibo/search')
@view('result_weibo')
@deco_get_keywords
def get_weibo_result(keyword, pos):
    (pre, cur, post) = gen_pos(pos)
    s = WeiboSearch()
    results = s.get_results(keyword, pos)
    query = dict(keyword = keyword, theme = 'weibo', pre = pre, cur = cur, post = post)
    return dict(weibos = results, weibo_actived = True, query = query)

@app.route('/blog/search/<keyword>/<pos:int>')
@app.post('/blog/search')
@view('result_blog')
def get_blog_result(keyword = None, pos = 0):
    if not keyword:
        keyword = request.forms.get('keyword')
        pos = int(request.forms.get('pos'))

    (pre, cur, post) = gen_pos(pos)

    s = BlogSearch()
    blogs = s.get_results(keyword, pos);

    query = dict(keyword = keyword, theme = 'blog', pre = pre, cur = cur, post = post)
    return dict(blogs = blogs, cctests = cctests, blog_actived = True, query = query)

#[demo]
@app.route('/scholar/1')
@view('scholar1')
def result():
    query = dict(keyword = 'scholar', theme = 'scholar', pre_pos = 0, cur_pos =0, post_pos = 0)
    return dict(scholar_actived = True, query = query)
 
@app.route('/scholar/2')
@view('scholar2')
def result():
    query = dict(keyword = 'scholar', theme = 'scholar', pre_pos = 0, cur_pos =0, post_pos = 0)
    return dict(scholar_actived = True, query = query)

@app.route('/scholar/3')
@view('scholar3')
def result():
    query = dict(keyword = 'scholar', theme = 'scholar', pre_pos = 0, cur_pos =0, post_pos = 0)
    return dict(scholar_actived = True, query = query)

@app.route('/scholar/4')
@view('scholar4')
def result():
    query = dict(keyword = 'scholar', theme = 'scholar', pre_pos = 0, cur_pos =0, post_pos = 0)
    return dict(scholar_actived = True, query = query)

@app.route('/scholar/search1/')
@app.post('/scholar/search1/')
@view('result_scholar')
def result():
    keyword = request.forms.get('keyword')
    scholars = jsonlist.get_scholars1(keyword)
    cctests = jsonlist.get_cctests1(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'scholar', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(scholars = scholars, cctests = cctests, scholar_actived = True, query = query)

@app.route('/scholar/search2/')
@app.post('/scholar/search2/')
@view('result_scholar')
def result():
    keyword = request.forms.get('keyword')
    scholars = jsonlist.get_scholars2(keyword)
    cctests = jsonlist.get_cctests2(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'scholar', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(scholars = scholars, cctests = cctests, scholar_actived = True, query = query)

@app.route('/scholar/search3/')
@app.post('/scholar/search3/')
@view('result_scholar')
def result():
    keyword = request.forms.get('keyword')
    scholars = jsonlist.get_scholars3(keyword)
    cctests = jsonlist.get_cctests3(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'scholar', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(scholars = scholars, cctests = cctests, scholar_actived = True, query = query)

@app.route('/weibo/search1/')
@app.post('/weibo/search1/')
@view('result_weibo')
def result(keyword = 'big data'):
    keyword = request.forms.get('keyword')
    cctests = jsonlist.get_cctests1(keyword)
    weibos = jsonlist.get_weibos1(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'weibo', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(weibos = weibos, cctests = cctests, weibo_actived = True, query = query)

@app.route('/weibo/search2/')
@app.post('/weibo/search2/')
@view('result_weibo')
def result(keyword = 'shujujicheng'):
    keyword = request.forms.get('keyword')
    cctests = jsonlist.get_cctests2(keyword)
    weibos = jsonlist.get_weibos2(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'weibo', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(weibos = weibos, cctests = cctests, weibo_actived = True, query = query)

@app.route('/weibo/search3/')
@app.post('/weibo/search3/')
@view('result_weibo')

def result(keyword = 'unstructure data'):
    keyword = request.forms.get('keyword')
    cctests = jsonlist.get_cctests3(keyword)
    weibos = jsonlist.get_weibos3(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'weibo', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(weibos = weibos, cctests = cctests, weibo_actived = True, query = query)

@app.route('/blog/search1/')
@app.post('/blog/search1/')
@view('result_blog')
def result(keyword = 'big data'):
    keyword = request.forms.get('keyword')
    cctests = jsonlist.get_cctests1(keyword)
    blogs = jsonlist.get_blogs1(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'blog', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(blogs = blogs, cctests = cctests, blog_actived = True, query = query)

@app.route('/blog/search2/')
@app.post('/blog/search2/')
@view('result_blog')
def result(keyword = 'shujujicheng'):
    keyword = request.forms.get('keyword')
    cctests = jsonlist.get_cctests2(keyword)
    blogs = jsonlist.get_blogs2(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'blog', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(blogs = blogs, cctests = cctests,  blog_actived = True, query = query)

@app.route('/blog/search3/')
@app.post('/blog/search3/')
@view('result_blog')
def result(keyword = 'unstructure data'):
    keyword = request.forms.get('keyword')
    cctests = jsonlist.get_cctests3(keyword)
    blogs = jsonlist.get_blogs3(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'blog', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(blogs = blogs, cctests = cctests, blog_actived = True, query = query)

@app.route('/patent/search1/')
@app.post('/patent/search1/')
@view('result_patent')
def result(keyword = 'big data'):
    keyword = request.forms.get('keyword')
    cctests = jsonlist.get_cctests1(keyword)
    patents = jsonlist.get_patents1(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'patent', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(patents = patents, cctests = cctests,  patent_actived = True, query = query)

@app.route('/patent/search2/')
@app.post('/patent/search2/')
@view('result_patent')
def result(keyword = 'shujujicheng'):
    keyword = request.forms.get('keyword')
    cctests = jsonlist.get_cctests2(keyword)
    patents = jsonlist.get_patents2(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'patent', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(patents = patents,  cctests = cctests, patent_actived = True, query = query)

@app.route('/patent/search3/')
@app.post('/patent/search3/')
@view('result_patent')
def result(keyword = 'unstructure data'):
    keyword = request.forms.get('keyword')
    cctests = jsonlist.get_cctests3(keyword)
    patents = jsonlist.get_patents3(keyword)
    pre_pos = 0
    post_pos = 0
    cur_pos = 0
    query = dict(keyword = keyword, theme = 'patent', pre_pos = pre_pos, cur_pos = cur_pos, post_pos = post_pos)
    return dict(patents = patents,  cctests = cctests, patent_actived = True, query = query)

# [Other]
@app.get('/static/<filename:path>')
def staticfile(filename):
    return static_file(filename, root='./static')

@error(404)
def error404(error):
    return 'OOps, NOT found!'

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True, reloader=True)
