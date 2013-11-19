# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import pymongo
from pymongo import Connection
import os
reload(sys)
sys.setdefaultencoding("utf-8")
connection=Connection('10.77.20.50',27017)
db=connection.academi
collection=db.scholar_meta

ifilename='names_in_dblp_not_in_ms'
ifile=open(ifilename,'r')

print 'aaa'
lines=ifile.readlines()
i=1

for line in lines:
	#id=i+54337692-1
	collection.insert({'has_photo':0, 
	'affiliation':None, 'ban':0,'email':'', 'homepage':'',
	'name':line[:-1],'name_low_case':line[:-1].lower(), 'native_name':'',
	'photo':'', 'scholar_id':str(i+54337692-1), 'from':'DBLP'})

	#print i
	print i+54337692-1
	#print line[:-1].lower()
	#print line
	#print line[:-1]
	
	i=i+1

ifile.close()