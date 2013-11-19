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

school='schools'
school_file=open(school,'r')
scholar='reviewer.xml'
scholar_file=open(scholar,'r')
scholars=scholar_file.readlines()
schools=school_file.readlines()
for i in schools:

	schoolname=i.split('	')[0]

	print schoolname
	m=2
	for ii in scholars:
		if (m%2==0):
			#print scholars[m-2][:-1]+scholars[m-1]
	
			#print scholars[m-2][:-1]+scholars[m-1]
			dom1=minidom.parseString(scholars[m-2][:-1]+scholars[m-1])
			root=dom1.documentElement
			#print root.childNodes
			node=root.getElementsByTagName('org_name')
			#print m-1
			#if (m==3526):
				#print (node[0].childNodes==[])
			#print node[0].childNodes
			#print node,m-1
			if (node!=[]):
				if (node[0].childNodes!=[]):
					sn=node[0].childNodes[0].nodeValue
					#print schoolname
					#print sn
					#print m-1
					if (sn.encode('gbk') ==schoolname.encode('gbk') ):
						#print schoolname
						#print sn
						scname=i.split('	')[1]
						node2=root.getElementsByTagName('psn_name')
						#print node2
						tname=node2[0].childNodes[0].nodeValue
						mail=root.getElementsByTagName('email')[0].childNodes[0].nodeValue
						#print tname[:-1]
						for item in collection.find({'affiliation':scname[:-1],'native_name':tname}):
							#collection.insert({'email':mail})
							collection.update({'affiliation':scname[:-1],'native_name':tname},{"$set":{'email':mail}})
							print root.getElementsByTagName('psn_name')[0].childNodes[0].nodeValue
							print mail
						#node2=root.getElementsByTagName('psn_name')
						#print node2[0].childNodes[0].nodeValue
		m=m+1

	



