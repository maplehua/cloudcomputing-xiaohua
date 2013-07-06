from app import mongo_conn
from pymongo import Connection
import random
def about_readmongo(about_type):
    jsonlist=[]
    connection=Connection('10.77.20.50',27017)
    db=connection.academi
    collection=db[about_type]
    mini=0
    maxi=collection.count()
    i=random.randint(mini,maxi)
    ii=i+20
    while ( i < ii ):
        if not (collection.find().skip(i).limit(-1).next()):
            i=0
        a = collection.find().skip(i).limit(-1).next()
        jsonlist.append(a)
        i=i+1
    return jsonlist
