# -*- coding: utf-8 -*-
#!/usr/bin/python
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
#import sys
import pymongo
from pymongo import Connection
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
connection=Connection('10.77.20.50',27017)
db=connection.academi
collection=db.paper_meta
result='names_from_dblp'
resultfile=open(result,'w')

a=1
for m in collection.find():
	for mm in m['authors']:
		resultfile.write(mm)
		resultfile.write('\n')
		a=a+1
print a

resultfile.close()
						

	



