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
    paper_id         = db.StringField()
    dblp_id          = db.StringField(db_field = 'key')
    title            = db.StringField(required = True)
    paper_type       = db.StringField(db_field = 'type')
    year             = db.StringField()
    month            = db.StringField()
    authors          = db.ListField(db.StringField())
    authors_low_case = db.ListField(db.StringField())
    ccf_rank         = db.StringField()
    journal          = db.StringField()
    booktitle        = db.StringField()

class ScholarMeta(db.Document):
    scholar_id    = db.StringField()
    ban           = db.IntField()
    name          = db.StringField()
    name_low_case = db.StringField()
    native_name   = db.StringField()
    affiliation   = db.StringField()
    email         = db.StringField()
    homepage      = db.StringField()
    photo         = db.StringField()

    def __repr__(self):
        return '<Scholar %r: %r>' % (self.scholar_id, self.name)

    def get_papers(self):
        return PaperMeta.objects(authors = self.name).order_by('-year')

    def get_scholars_by_name(sch_name):
        scholars =  ScholarMeta.objects(name_low_case = sch_name.lower(), ban = 0)
        if scholars.count() == 0:
            if PaperMeta.objects(authors_low_case = sch_name.lower()).count() > 0:
                scholar = ScholarMeta(name = keyword.title(), scholar_id = '0')
                return [scholar]
        return scholars

    def get_scholar_by_id(sch_id):
        if scholar_id == '0':
            scholar = ScholarMeta(name = name.title())
        else:
            scholar = ScholarMeta.objects(scholar_id = scholar_id).first_or_404()
        return scholar

class Affiliation(db.Document):
    name     = db.StringField()
    scholars = db.ListField(db.StringField())

    def __repr__(self):
        return '<Affiliation %r>' % (self.name)

    @classmethod
    def get_papers_by_affi_name(self, aff_name):
        affi = Affiliation.objects(name = aff_name).first()
        if affi:
            paper_all =  PaperMeta.objects(authors__in = affi.scholars).order_by('-year')
            paper_rank_a = paper_all.filter(ccf_rank = 'A')
            paper_rank_b = paper_all.filter(ccf_rank = 'B')
            paper_rank_c = paper_all.filter(ccf_rank = 'C')
            paper_rank_unknow = paper_all.filter(ccf_rank = 'unknow')
            return dict(paper_all = paper_all,
                paper_rank_a = paper_rank_a,
                paper_rank_b = paper_rank_b,
                paper_rank_c = paper_rank_c,
                paper_rank_unknow = paper_rank_unknow)
        else:
            return None

    @classmethod
    def stat_papers(self, papers):
        count_all = len(papers['paper_all'])
        count_rank_a = len(papers['paper_rank_a'])
        count_rank_b = len(papers['paper_rank_b'])
        count_rank_c = len(papers['paper_rank_c'])
        count_rank_unknow = count_all - count_rank_a - count_rank_b - count_rank_c
        prop_rank_a = count_rank_a * 100 / count_all
        prop_rank_b = count_rank_b * 100 / count_all
        prop_rank_c = count_rank_c * 100 / count_all
        prop_rank_unknow = (100 - prop_rank_a - prop_rank_b - prop_rank_c)
        return dict(count_all = count_all,
            count_rank_a = count_rank_a,
            count_rank_b = count_rank_b,
            count_rank_c = count_rank_c,
            count_rank_unknow = count_rank_unknow,
            prop_rank_a = prop_rank_a,
            prop_rank_b = prop_rank_b,
            prop_rank_c = prop_rank_c,
            prop_rank_unknow = prop_rank_unknow)

