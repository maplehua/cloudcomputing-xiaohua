from flask import abort, render_template, flash, redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, login_manager
from app.models import User
from forms import SearchForm, LoginForm
from search import AcademiSearch as Search
from about import about_readmongo
from config import *
from scholar_page import *

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(userid):
    return User.objects(id = userid).first()

@app.route('/')
@app.route('/index')
@app.route('/scholar')
def index_scholar():
    form = SearchForm()
    form.theme.data = 'scholar'
    return render_template('index_scholar.html',theme = 'scholar', form = form)

@app.route('/paper')
def index_paper():
    form = SearchForm()
    form.theme.data = 'paper'
    return render_template('index_paper.html',theme = 'paper', form = form)

@app.route('/university')
def index_affiliation():
    form = SearchForm()
    form.theme.data = 'affiliation'
    return render_template('index_affiliation.html',theme = 'affiliation', form = form)

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
    if theme == 'scholar' and len(result) == 1:
        user_id = result[0]['scholar_id']
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
    #pages = about_readmongo("about_page")
    #papers = about_readmongo("about_paper")
    #weibos = about_readmongo("about_weibo")
    #return render_template('about.html', pages = pages, papers = papers, weibos = weibos)
    abort(404)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        flash('Success login.')
        user = form.get_user()
        login_user(user)
        return redirect('/admin')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

