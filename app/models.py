import uuid
from app import mongo_conn, es_conn
from config import PAPER_COLLECTION, MONGODB_DB

class Paper():
    def __init__(self):
        self.uuid = unicode(uuid.uuid1())
        self.title = title
        self.authors = authors
        self.source = source
        self.year = year
        self.body = body
        self.language = language

    def to_dict(self):
        return dict(uuid = self.uuid,
                title = self.title,
                authors = self.authors,
                source = self.source,
                year = self.year,
                body = self.body,
                language = self.language)

    def from_dict(self, j):
        self.uuid = j.uuid
        self.title = j.title
        self.authors = j.authors
        self.source = j.source
        self.year = j.year
        self.body = j.body
        self.language = j.language

    def __repr__(self):
        return '<Paper %r> %r' % (self.uuid, self.title)
