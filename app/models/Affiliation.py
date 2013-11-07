from app import mongo_db as db
from app.models.PaperMeta import PaperMeta

class Affiliation(db.Document):
    #aff_id   = db.IntField()
    name     = db.StringField()
    scholars = db.ListField(db.StringField())

    def __repr__(self):
        return '<Affiliation %r>' % (self.name)

    def __unicode__(self):
        return self.name

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
