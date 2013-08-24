from flask import abort, render_template, flash, redirect, url_for, request
from app import app, redis_conn
from forms import SearchForm
from search import AcademiSearch as Search
from about import about_readmongo
from config import *
from scholar_page import *

@app.route('/paper')
def index_paper():
    form = SearchForm()
    form.theme.data = 'paper'
    return render_template('index_paper.html',theme = 'paper', form = form)

@app.route('/')
@app.route('/scholar')
@app.route('/index')
def index_scholar():
    form = SearchForm()
    form.theme.data = 'scholar'
    return render_template('index_scholar.html',theme = 'scholar', form = form)
@app.route('/paper_en')
def index_paper_en():
    form = SearchForm()
    form.theme.data = 'paper_en'
    return render_template('index_paper_en.html', theme = 'paper_en', form = form)

#@app.route('/scholar')
@app.route('/patent')
@app.route('/weibo')
@app.route('/blog')
def to_implement():
    abort(404)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        request_form = SearchForm(request.form)
        if not request_form.validate_on_submit():
            return redirect(url_for('index'))
        keyword = request_form.keyword.data
        theme = request_form.theme.data
        offset = request_form.offset.data
    else:
        keyword = request.args.get('keyword')
        theme = request.args.get('theme')
        offset = request.args.get('offset')

    s = Search(theme = theme, keyword = keyword, offset = offset)
    result = s.result()

    form = SearchForm()
    form.theme.data = theme

    # hack fix for scholar search
    if theme == 'scholar_single':
        form.theme.data = 'scholar'

    #deal with the scholar theme separately
    if theme == 'scholar' and result['total'] == 1:
        user_id = result['scholars'][0]['user_id']
        theme = 'scholar_single'
        s = Search(theme = theme, keyword = keyword, offset = user_id)
        result = s.result()

    meta = {'theme': theme,
            'offset': offset,
            'keyword': keyword}

    template = 'result_%s.html' % theme

    return render_template(template,
        meta = meta,
        form = form,
        result = result)

@app.route('/about')
def about():
    pages = about_readmongo("about_page")
    papers = about_readmongo("about_paper")
    weibos = about_readmongo("about_weibo")
    return render_template('about.html', pages = pages, papers = papers, weibos = weibos)

@app.route('/api/stat/net')
def api():
    return str(int(float(redis_conn.get('about_number'))))

