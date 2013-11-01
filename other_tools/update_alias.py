# -*- coding: utf-8 -*-
#!/usr/bin/python
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import sys
import pymongo
from pymongo import Connection
import os

connection=Connection('10.77.20.50',27017)
db=connection.academi
collection=db.scholar_meta


reload(sys)
sys.setdefaultencoding("utf-8")

namelist='namelist.txt'
name_file=open(namelist,'r')
names=name_file.readlines()

#collection.update({},{"$set":{'alias':'mail'}},True,True)
#print collection.findones()

for m in collection.find():
	namelist=[]
	namelist.append( m['name'])
	collection.update(m,{"$set":{'alias':namelist}})
print 'step one over'
updateNumber=0
for i in names:
	#print i.encode("gbk")


	name=i.split('		')[0]
	alias=i.split('		')[1]
	a=[] 
	
	for i in alias.split(','):
		if (i[-1:]=='\n'):
			a.append(i[:-1])
		else:

			a.append(i)
			#print name
			#print a

	
	for item in collection.find({'name':name[:-1]}):
		a.append(item['name'])
		#print item['name']
		#print a
		collection.update(item,{"$set":{'alias':a}})
		updateNumber=updateNumber+1
		#print name[:-1]
		#print 1
print updateNumber
print 'step two over'

						
		#print name
						

	



