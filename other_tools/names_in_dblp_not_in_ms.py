# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import pymongo
from pymongo import Connection
import os

connection=Connection('10.77.20.50',27017)
db=connection.academi
collection=db.scholar_meta

ofilename='names_in_dblp_not_in_ms'
ofile=open(ofilename,'w')
reload(sys)
sys.setdefaultencoding("utf-8")
ifilename='names_from_dblp2'
ifile=open(ifilename,'r')
lines=ifile.readlines()
i=0
ii=0
for line in lines:
	ii=ii+1
	#print line
	#print line[:-1]
	if (ii%100==0):
		print ii
	if (collection.find_one({'name':line[:-1]})==None):
		i=i+1
		ofile.write(line)
		#print line
		#print line[:-1]
print i
print ii
if( collection.find_one({'name':'Jiaheng Lu'})!=None):
	print '= =!'

print 'lalala\n'

if ( collection.find_one({'name':'Caiyun Yao'})==None):
	print '= ='
ofile.close()