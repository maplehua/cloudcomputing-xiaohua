from flask.ext.login import UserMixin
from app import mongo_db as db

class User(db.Document, UserMixin):
    username = db.StringField(max_length = 255, required = True)
    password = db.StringField(max_length = 255, required = True)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def __unicode__(self):
        return self.username

class PaperMeta(db.Document):
    paper_id = db.StringField()
    dblp_id = db.StringField(db_field = 'key')
    title = db.StringField(required = True)
    paper_type = db.StringField(db_field = 'type')
    year = db.StringField()
    month = db.StringField()
    authors = db.ListField(db.StringField())
    authors_low_case = db.ListField(db.StringField())
    ccf_rank = db.StringField()
    journal = db.StringField()
    booktitle = db.StringField()

class ScholarMeta(db.Document):
    scholar_id = db.StringField()
    ban = db.IntField()
    name = db.StringField()
    name_low_case = db.StringField()
    native_name = db.StringField()
    affiliation = db.StringField()
    email = db.StringField()
    homepage = db.StringField()
    photo = db.StringField()

    def __repr__(self):
        return '<Scholar %r: %r>' % (self.scholar_id, self.name)

    def get_scholar_by_id(scholar_id):
        return ScholarMeta.objects.get_or_404(scholar_id = scholar_id)

    def get_scholar_by_low_case_name(name):
        return ScholarMeta.objects.get_or_404(name)

class Affiliation(db.Document):
    name = db.StringField()
    scholar_names = db.ListField(db.StringField())

    def __repr__(self):
        return '<Affiliation %r>' % (self.name)

