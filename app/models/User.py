from flask.ext.login import UserMixin
from app import mongo_db as db

class User(db.Document, UserMixin):
    username = db.StringField(max_length = 255, required = True)
    password = db.StringField(max_length = 255, required = True)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def __unicode__(self):
        return self.username
