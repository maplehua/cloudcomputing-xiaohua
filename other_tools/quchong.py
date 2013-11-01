#!/usr/bin/python

#run in python 2.X #
# -*- coding:utf-8 -*-
ifd=file("names_from_dblp","r")
ofd=file("sortedoutput.txt", "w")
list1=[]
lines=ifd.readlines()
i=0
for line in lines:
	list1.append(line)
	i=i+1

print i
