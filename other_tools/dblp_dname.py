# -*- coding: utf-8 -*-
#!/usr/bin/python
import os
from bs4 import BeautifulSoup
from bs4 import BeautifulStoneSoup
import bs4

file1name='Y:\\Xin\\dblp\\author_list_20130401_2\\11\\Rajyalakshmi.S=.html'
file1=open(file1name,'r')
lines=file1.readlines()
a=''
for line in lines:
	a=a+line
soup=BeautifulSoup(a)
print type(soup)
print soup.find('h1')
if (soup.find('h1')!=None):
	print soup.find('h1').next.encode('utf-8') 
print soup.findAll('p')

file2=open('E:\\dname','w')


for abc in os.walk('Y:\\Xin\\dblp\\author_list_20130401_2'):
	print abc[0]
	for abcd in abc[1]:
		print abcd
		for abcde in os.walk('Y:\\Xin\\dblp\\author_list_20130401_2\\'+abcd):
			for abcdef in abcde[2]:
				print 'Y:\\Xin\\dblp\\author_list_20130401_2\\'+abcd+'\\'+abcdef
				file1name='Y:\\Xin\\dblp\\author_list_20130401_2\\'+abcd+'\\'+abcdef
				file1=open(file1name,'r')
				lines=file1.readlines()
				a=''
				for line in lines:
					a=a+line
				soup=BeautifulSoup(a)
				print type(soup)
				if (soup.find('h1')!=None):
					print soup.find('h1').next.encode('utf-8')
					
					if (soup.find('p')!=None):
						print soup.find('p') 
						file2.write(soup.find('h1').next.encode('utf-8'))
						file2.write('		')
						file2.write(soup.find('p').next.encode('utf-8'))
						file2.write('\n')
				#print soup.findAll('p')
file2.close()


