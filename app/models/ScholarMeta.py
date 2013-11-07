from app import mongo_db as db
from app.models.PaperMeta import PaperMeta

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

    @classmethod
    def get_autocomplete_names(self, keyword):
        return ScholarMeta.objects(name__istartswith = keyword, ban = 0).only('name', 'scholar_id').limit(15).to_json()

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

