# -*- coding: utf-8 -*-
#!/usr/bin/python
#import os
from bs4 import BeautifulSoup
from bs4 import BeautifulStoneSoup
import bs4


file1name='E:\\dnameplus'
file1=open(file1name,'r')
file2name='E:\\dnameplusplus'
file2=open(file2name,'w')

lines=file1.readlines()
for line in lines:
	content=line.split('		')

	if (content[1].find('Univ.')<0):
		#print content[0]
		print 1
		file2.write(line)
file2.close()
