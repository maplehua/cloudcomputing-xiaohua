from app import mongo_db as db

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

    def __repr__(self):
        return '<Paper %r: %r>' % (self.paper_id, self.title)

    def __unicode__(self):
        return self.title

    @classmethod
    def get_papers(self, page = 1):
        return PaperMeta.objects.paginate(page = page, per_page = 10)
