from bson import json_util
from flask import abort, render_template, flash, redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, login_manager
from app.models.User import User
from app.models.ScholarMeta import ScholarMeta
from app.models.Affiliation import Affiliation
from forms import SearchForm, LoginForm
from search import AcademiSearch as Search
from pymongo import MongoClient
from bson import ObjectId

from config import *

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

@app.route('/keyword')
@app.route('/keyword/<key>')
def keyword(key=None):
    return render_template('page.html',key=key)

@app.route('/info')
def info():
    g.client=MongoClient("10.77.20.50")
    g.db=g.client['article'] 
    g.col=g.db['info']
    results=g.col.find({'set':request.args.get('set'),'number':request.args.get('number')})
    return render_template("article_info.html",results=results)


@app.route('/require',methods=['GET','POST'])
def require():
    if request.method == 'POST':
        g.client=MongoClient("10.77.20.50")
        g.db=g.client['extract'];
        results=g.db.command("text","data",search=request.form['searchKey'],limit=10)['results']
    return render_template('page.html',key=request.form['searchKey'],results=results)
    
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
    is_post =  request.method == 'POST'
    if is_post:
        request_form = SearchForm(request.form)
        if not request_form.validate_on_submit():
            return redirect(url_for('index_scholar'))

    keyword = request_form.keyword.data if is_post else request.args.get('keyword')
    theme = request_form.theme.data if is_post else request.args.get('theme')
    offset = request_form.offset.data if is_post else request.args.get('offset')
    page = request_form.page.data if is_post else request.args.get('page')
 
    if theme=='scholar':
       return redirect('/scholar/%s' % (keyword.replace(' ','_')+'.html')) 
    s = Search(theme = theme, keyword = keyword, offset = offset, page = page)
    result = s.result()

    form = SearchForm()
    # hack fix for converting scholar_* to scholar
    form.theme.data =  theme.split('_')[0]

    #deal with the scholar theme separately
    if theme == 'scholar' and len(result) == 1:
        user_id = result[0]['scholar_id']
        theme = 'scholar_single'
        s = Search(theme = theme, keyword = keyword, offset = user_id)
        offset = user_id
        result = s.result()

    meta = {'theme': theme,
            'offset': offset,
            'keyword': keyword,
            'page': page}

    template = 'result_%s.html' % theme

    return render_template(template,
        meta   = meta,
        form   = form,
        result = result)

@app.route('/scholar/<scholar_name>')
def scholar(scholar_name):
    scholar_name=scholar_name[:-5]
    #whether has ID
    if(scholar_name.split('_')[-1].isdigit()):
        scholar_id = scholar_name.split('_')[-1]
        scholar_name = scholar_name.split('_')[:-1]
        scholar_name = ' '.join(scholar_name)
        theme = 'scholar_single'
        offset = scholar_id
        s = Search(theme = 'scholar_single', keyword = scholar_name, offset = scholar_id, page = 1)

    else :
        theme = 'scholar'
        offset = 0
        scholar_name = scholar_name.split('_')
        scholar_name = ' '.join(scholar_name)
        scholar_name = scholar_name.encode("utf-8")
        s = Search(theme = 'scholar', keyword = scholar_name, offset = 0, page = 1)
   
    result = s.result()
    form = SearchForm()
    # hack fix for converting scholar_* to scholar
    form.theme.data =  theme.split('_')[0]
 
    #deal with the scholar theme separately
    if theme == 'scholar' and len(result) == 1:
        user_id = result[0]['scholar_id']
        theme = 'scholar_single'
        s = Search(theme = theme, keyword = scholar_name, offset = user_id)
        offset = user_id
        result = s.result()

    meta = {'theme': theme,
            'offset': offset,
            'keyword': scholar_name,
            'page': 1}

    template = 'result_%s.html' % theme

    return render_template(template,
        meta   = meta,
        form   = form,
        result = result)


@app.route('/about')
def about():
    return render_template('about.html')

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

@app.route('/ajax/<theme>')
def ajax(theme):
    keyword = request.args.get('query')
    if theme == 'scholar':
        name_list = ScholarMeta.get_autocomplete_names(keyword)
    elif theme == 'affiliation':
        name_list =  Affiliation.get_autocomplete_names(keyword)
    else:
        name_list = []
    return name_list
