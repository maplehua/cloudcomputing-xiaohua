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
    pages            = db.StringField()

    @classmethod
    def get_papers(self, page = 1):
        return PaperMeta.objects.paginate(page = page, per_page = 10)

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

    @classmethod
    def get_papers(self, sch_name, ccf_rank = None, page = 1):
        papers = PaperMeta.objects(authors_low_case = sch_name.lower()).order_by('-year')
        if ccf_rank:
            papers = papers.filter(ccf_rank = ccf_rank)
        page = int(page) if page else 1
        return papers.paginate(page = int(page), per_page = 10)

    @classmethod
    def stat_papers(self, sch_name):
        papers = PaperMeta.objects(authors_low_case = sch_name.lower())
        count_all = len(papers)
        count_rank_a = len(papers.filter(ccf_rank = 'A'))
        count_rank_b = len(papers.filter(ccf_rank = 'B'))
        count_rank_c = len(papers.filter(ccf_rank = 'C'))
        count_rank_unknow = count_all - count_rank_a - count_rank_b - count_rank_c
        prop_rank_a = (count_rank_a * 100 / count_all) if count_all else 0
        prop_rank_b = (count_rank_b * 100 / count_all) if count_all else 0
        prop_rank_c = (count_rank_c * 100 / count_all) if count_all else 0
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
    def get_papers(self, aff_name, ccf_rank = None, page = 1):
        affi = Affiliation.objects(name = aff_name).first()
        papers = PaperMeta.objects(authors__in = affi.scholars).order_by('-year') if affi else []
        if ccf_rank:
            papers = papers.filter(ccf_rank = ccf_rank)
        #page = int(page) if page else 1
        return papers.paginate(page = int(page), per_page = 10) if affi else None


    @classmethod
    def stat_papers(self, aff_name):
        affi = Affiliation.objects(name = aff_name).first()
        count_all = PaperMeta.objects(authors__in = affi.scholars).count() if affi else 0
        count_rank_a = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'A').count() if affi else 0
        count_rank_b = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'B').count() if affi else 0
        count_rank_c = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'C').count() if affi else 0
        count_rank_unknow = count_all - count_rank_a - count_rank_b - count_rank_c
        prop_rank_a = (count_rank_a * 100 / count_all) if count_all else 0
        prop_rank_b = (count_rank_b * 100 / count_all) if count_all else 0
        prop_rank_c = (count_rank_c * 100 / count_all) if count_all else 0
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


     @classmethod
     def get_year_papers(self,aff_name)
         affi = Affiliation.objects(name = aff_name).first()
         count_all = PaperMeta.objects(authors__in = affi.scholars).count() if affi else 0
         count_rank_a_2013 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'A', year = "2013").count() if affi else 0
         count_rank_b_2013 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'B', year = "2013").count() if affi else 0
         count_rank_c_2013 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'C', year = "2013").count() if affi else 0
         count_rank_a_2012 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'A', year = "2012").count() if affi else 0
         count_rank_b_2012 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'B', year = "2012").count() if affi else 0
         count_rank_c_2012 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'C', year = "2012").count() if affi else 0
         count_rank_a_2011 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'A', year = "2011").count() if affi else 0
         count_rank_b_2011 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'B', year = "2011").count() if affi else 0
         count_rank_c_2011 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'C', year = "2011").count() if affi else 0
         count_rank_a_2010 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'A', year = "2010").count() if affi else 0
         count_rank_b_2010 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'B', year = "2010").count() if affi else 0
         count_rank_c_2010 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'C', year = "2010").count() if affi else 0
         count_rank_a_2009 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'A', year = "2009").count() if affi else 0
         count_rank_b_2009 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'B', year = "2009").count() if affi else 0
         count_rank_c_2009 = PaperMeta.objects(authors__in = affi.scholars, ccf_rank = 'C', year = "2009").count() if affi else 0
         return dict(count_rank_a_2013=count_rank_a_2013,
                    count_rank_a_2013=count_rank_a_2013,
                    count_rank_a_2013=count_rank_a_2013,
                    count_rank_a_2013=count_rank_a_2012,
                    count_rank_a_2013=count_rank_a_2012,
                    count_rank_a_2013=count_rank_a_2012,
                    count_rank_a_2013=count_rank_a_2011,
                    count_rank_a_2013=count_rank_a_2011,
                    count_rank_a_2013=count_rank_a_2011,
                    count_rank_a_2013=count_rank_a_2010,
                    count_rank_a_2013=count_rank_a_2010,
                    count_rank_a_2013=count_rank_a_2010,
                    count_rank_a_2013=count_rank_a_2009,
                    count_rank_a_2013=count_rank_a_2009,
                    count_rank_a_2013=count_rank_a_2009)
         
         
         
         
         

