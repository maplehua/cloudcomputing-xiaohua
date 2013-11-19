#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymongo
from pymongo import Connection
def about_readmongo(about_type):
	jsonlist=""
	connection=Connection('10.77.20.50',27017)
	db=connection.academi
	collection=db.about_weibo
	i=0
	while ( i < 30 ):
		jsonlist=jsonlist+str(collection.find().skip(i).limit(-1).next())
#		print collection.find().skip(i).limit(-1).next()
		i=i+1
	print i
	return jsonlist

if __name__=='__main__':
	list1=about_readmongo("about_weibo")
	print list1