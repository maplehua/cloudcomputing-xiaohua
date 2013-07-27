from flask.ext.wtf import Form, TextField, widgets
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.pymongo import ModelView

class PaperForm(Form):
    title = TextField('title')
    year = TextField('year')
    publication = TextField('publication')
    uuid = TextField('uuid')
    authors = TextField('authors')

class PaperView(ModelView):
    column_list = ('uuid', 'title', 'publication', 'year', 'authors')
    column_searchable_list = ('title', 'publication', 'year')
    form = PaperForm

class ScholarPaperForm(Form):
    title = TextField('title')
    year = TextField('year')
    type = TextField('type')
    authors = TextField('authors')

class ScholarPaperView(ModelView):
    column_list = ('paper_id', 'title', 'type','year','authors')
    column_searchable_list = ('authors')
    form = ScholarPaperForm
