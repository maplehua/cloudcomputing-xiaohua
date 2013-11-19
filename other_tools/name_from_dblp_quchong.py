#!/usr/bin/python

#run in python 2.X #
# -*- coding:utf-8 -*-
ifd=file("names_from_dblp","r")
ofd=file("names_from_dblp2", "w")
list1=[]
lines=ifd.readlines()
i=0
for line in lines:
	list1.append(line)
	i=i+1

print i

ii=0
list2=list(set(list1))

for line2 in list2:
	ii=ii+1
	ofd.write(line2)
print ii
ofd.close()
