from app import mongo_db as db
from app.models.PaperMeta import PaperMeta

class CCF_Stat(db.EmbeddedDocument):
    a = db.IntField()
    b = db.IntField()
    c = db.IntField()
    u = db.IntField()

class Stat(db.EmbeddedDocument):
    total = db.IntField()
    ccf = db.EmbeddedDocumentField(document_type = CCF_Stat)

    def prop(self, n):
        return n * 100 / self.total

class Affiliation(db.Document):
    aff_id   = db.IntField()
    name     = db.StringField()
    scholars = db.ListField(db.StringField())
    stat     = db.EmbeddedDocumentField(document_type = Stat)
    logo     = db.StringField()

    def __repr__(self):
        return '<Affiliation %r>' % (self.name)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_autocomplete_names(self, keyword):
        return Affiliation.objects(name__istartswith = keyword).order_by('-stat.total').only('name', 'stat.total').limit(10).to_json()

    @classmethod
    def get_affiliation(self, aff_name):
        return Affiliation.objects(name__iexact = aff_name).first_or_404()

    def get_papers(self, ccf_rank = None, page = 1):
        papers = PaperMeta.objects(authors__in = self.scholars).order_by('-year')
        if ccf_rank:
            papers = papers.filter(ccf_rank = ccf_rank)
        return papers.paginate(page = int(page), per_page = 10)

    def stat_papers(self):
        stat_dict = {}

        pa = self.stat.prop(self.stat.ccf.a)
        pb = self.stat.prop(self.stat.ccf.b)
        pc = self.stat.prop(self.stat.ccf.c)
        pu = 100 - pa - pb - pc
        return dict(count_all = self.stat.total,
            count_rank_a = self.stat.ccf.a,
            count_rank_b = self.stat.ccf.b,
            count_rank_c = self.stat.ccf.c,
            count_rank_unknow = self.stat.ccf.u,
            prop_rank_a = pa,
            prop_rank_b = pb,
            prop_rank_c = pc,
            prop_rank_unknow = pu)

    def get_year_papers(self):
        paper_all = PaperMeta.objects(authors__in = self.scholars)
        count_rank_a_2013 = paper_all.filter(ccf_rank = 'A', year = "2013").count()
        count_rank_b_2013 = paper_all.filter(ccf_rank = 'B', year = "2013").count()
        count_rank_c_2013 = paper_all.filter(ccf_rank = 'C', year = "2013").count()
        count_rank_a_2012 = paper_all.filter(ccf_rank = 'A', year = "2012").count()
        count_rank_b_2012 = paper_all.filter(ccf_rank = 'B', year = "2012").count()
        count_rank_c_2012 = paper_all.filter(ccf_rank = 'C', year = "2012").count()
        count_rank_a_2011 = paper_all.filter(ccf_rank = 'A', year = "2011").count()
        count_rank_b_2011 = paper_all.filter(ccf_rank = 'B', year = "2011").count()
        count_rank_c_2011 = paper_all.filter(ccf_rank = 'C', year = "2011").count()
        count_rank_a_2010 = paper_all.filter(ccf_rank = 'A', year = "2010").count()
        count_rank_b_2010 = paper_all.filter(ccf_rank = 'B', year = "2010").count()
        count_rank_c_2010 = paper_all.filter(ccf_rank = 'C', year = "2010").count()
        count_rank_a_2009 = paper_all.filter(ccf_rank = 'A', year = "2009").count()
        count_rank_b_2009 = paper_all.filter(ccf_rank = 'B', year = "2009").count()
        count_rank_c_2009 = paper_all.filter(ccf_rank = 'C', year = "2009").count()
        return dict(count_rank_a_2013=count_rank_a_2013,
                    count_rank_b_2013=count_rank_b_2013,
                    count_rank_c_2013=count_rank_c_2013,
                    count_rank_a_2012=count_rank_a_2012,
                    count_rank_b_2012=count_rank_b_2012,
                    count_rank_c_2012=count_rank_c_2012,
                    count_rank_a_2011=count_rank_a_2011,
                    count_rank_b_2011=count_rank_b_2011,
                    count_rank_c_2011=count_rank_c_2011,
                    count_rank_a_2010=count_rank_a_2010,
                    count_rank_b_2010=count_rank_b_2010,
                    count_rank_c_2010=count_rank_c_2010,
                    count_rank_a_2009=count_rank_a_2009,
                    count_rank_b_2009=count_rank_b_2009,
                    count_rank_c_2009=count_rank_c_2009)
