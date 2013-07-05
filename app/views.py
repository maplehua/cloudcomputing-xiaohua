from flask import abort, render_template, flash, redirect, session, url_for, request, g
from app import app
from forms import SearchForm
from search import AcademiSearch as Search
from config import *

@app.route('/')
@app.route('/paper')
@app.route('/index')
def index_paper():
    form = SearchForm()
    form.theme.data = 'paper'
    return render_template('index_paper.html',theme = 'paper', form = form)

@app.route('/paper_en')
def index_paper_en():
    form = SearchForm()
    form.theme.data = 'paper_en'
    return render_template('index_paper_en.html', theme = 'paper_en', form = form)

@app.route('/scholar')
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
    meta = {'theme': theme,
            'offset': offset,
            'keyword': keyword}

    return render_template('result_%s.html' % theme,
        meta = meta,
        form = form,
        result = result)

@app.route('/about')
def about():
    return render_template('about.html')
