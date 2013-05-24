#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymongo
import json
from pymongo import Connection
connection=Connection('10.77.20.50',27017)
db=connection.academi
collection=db.about_page
#注意文件编码类型改为：utf-8(不包含bom)
addressjson="E:\pages.txt"
i=0
input_file=open(addressjson,"r")
#while input_file:
#	addressjson="C:\Users\Leia\Desktop\onejson\onejson\onejson"+str(i)
#input_file=open(addressjson,"r")
#i=i+1
#allline=""

for line in input_file:
#	allline=allline+line
	try:
		print i
		print line
		line=json.loads(line)
		collection.insert(line)
		i=i+1
		print i
	except:
		pass
#print allline
input_file.close()
print i



