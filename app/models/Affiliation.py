from app import mongo_db as db
from app.models.PaperMeta import PaperMeta

class Stat(db.EmbeddedDocument):
    a = db.IntField()
    b = db.IntField()
    c = db.IntField()
    u = db.IntField()

    def total(self):
        return sum([self.a, self.b, self.c, self.u])

    def prop(self, n):
        return n * 100 / self.total()

class Affiliation(db.Document):
    aff_id   = db.IntField()
    name     = db.StringField()
    scholars = db.ListField(db.StringField())
    stat     = db.EmbeddedDocumentField(Stat)

    def __repr__(self):
        return '<Affiliation %r>' % (self.name)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_autocomplete_names(self, keyword):
        return Affiliation.objects(name__istartswith = keyword).only('name').limit(10).to_json()

    @classmethod
    def get_affiliation(self, aff_name):
        return Affiliation.objects(name__iexact = aff_name).first_or_404()

    def get_papers(self, ccf_rank = None, page = 1):
        papers = PaperMeta.objects(authors__in = self.scholars).order_by('-year')
        if ccf_rank:
            papers = papers.filter(ccf_rank = ccf_rank)
        return papers.paginate(page = int(page), per_page = 10)

    def stat_papers(self):
        pa = self.stat.prop(self.stat.a)
        pb = self.stat.prop(self.stat.b)
        pc = self.stat.prop(self.stat.c)
        pu = 100 - pa - pb - pc
        return dict(count_all = self.stat.total(),
            count_rank_a = self.stat.a,
            count_rank_b = self.stat.b,
            count_rank_c = self.stat.c,
            count_rank_unknow = self.stat.u,
            prop_rank_a = pa,
            prop_rank_b = pb,
            prop_rank_c = pc,
            prop_rank_unknow = pu)

    @classmethod
    def get_year_papers(self,aff_name):
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
