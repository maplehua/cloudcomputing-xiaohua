from flask.ext.wtf import Form, TextField, IntegerField, widgets
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.pymongo import ModelView, filters

class PaperForm(Form):
    title = TextField('title')
    year = TextField('year')
    publication = TextField('publication')
    uuid = TextField('uuid')
    authors = TextField('authors')

class PaperView(ModelView):
    column_list = ('uuid', 'title', 'publication', 'year', 'authors')
    column_searchable_list = ('publication', 'year')
    form = PaperForm

class ScholarPaperForm(Form):
    title = TextField('title')
    year = TextField('year')
    type = TextField('type')
    booktitle = TextField('booktitle')
    journal = TextField('journal')
    ccf_rank = TextField('ccf_rank')
    authors = TextField('authors')

class ScholarPaperView(ModelView):
    column_list = ('paper_id', 'title', 'type', 'booktitle', 'journal', 'ccf_rank', 'year','authors')
    #column_searchable_list = ('paper_id', 'authors')
    column_filters = (filters.FilterEqual('booktitle', 'booktitle'),
                filters.FilterLike('booktitle', 'booktitle'),
                filters.FilterEqual('journal', 'journal'),
                filters.FilterLike('journal', 'journal'),
                filters.FilterEqual('year', 'year'),
                filters.FilterLike('title', 'title'),
                )
    form = ScholarPaperForm

class ScholarForm(Form):
    user_id = TextField('user_id')
    invisible = IntegerField('invisible')
    Name = TextField('Name')
    NameLowCase = TextField('NameLowCase')
    NativeName = TextField('NativeName')
    Affiliation = TextField('Affiliation')
    Homepage = TextField('Homepage')
    Email = TextField('Email')
    HomepageIsDead = TextField('HomepageIsDead')
    HasPhoto = TextField('HasPhoto')
    DisplayPhotoURL = TextField('DisplayPhotoURL')
    Photo = TextField('Photo')

class ScholarView(ModelView):
    column_list = ('user_id', 'invisible', 'Name', 'NativeName', 'Affiliation', 'Homepage', 'Email')
    #column_searchable_list = ('user_id', 'NameLowCase')
    column_filters = (filters.FilterEqual('NameLowCase', 'NameLowCase'),
                filters.FilterEqual('user_id', 'user_id'))
    form = ScholarForm
