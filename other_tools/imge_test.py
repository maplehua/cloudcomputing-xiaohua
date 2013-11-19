#!/usr/bin/env python
#encoding=utf-8

import cStringIO, urllib2, Image
import xlrd
import base64
import pymongo
import json
from pymongo import Connection
import os


def make_post_thumb(path, size=(96,96)):
	#base,ext=os.path.splitext(path)
	try:
		im=Image.open(path)
	except IOError:
		print 'in IOError'
		return
	mode=im.mode
	print mode

	width,height=im.size

	#for size in sizes:
	filename='temp'+'.jpg'
	if float(width)/float(height)==float(str(size[0]))/float(str(size[1])):
		im_1200=im.resize(size[0],size[1],Image.ANTIALIAS)
		im_1200.save(filename,quality=100)
	if float(width)/float(height)>float(size[0])/float(size[1]):
		im_1200=im.resize((int(size[0]),int(float(height)/(float(width)/float(size[0])))),Image.ANTIALIAS)
		im_1200_width,im_1200_height=im_1200.size
		#delta=(im_1200_height-int(size[1]))/2
		box=(0,0,im_1200_width, im_1200_height)
		region=im_1200.crop(box)
		merge_img=Image.new('RGB',(96,96),0xFFFFFF)
		merge_img.paste(region,(0,(96-im_1200_height)/2))
		merge_img.save(filename,quality=100)
	if float(width)/float(height)<float(size[0])/float(size[1]):
		im_1200=im.resize((int(float(width)/(float(height)/float(size[1]))),int(size[1])),Image.ANTIALIAS)
		im_1200_width,im_1200_height=im_1200.size
		#delta=(im_1200_width-int(size[0]))/2
		box=(0,0,im_1200_width, im_1200_height)
		region=im_1200.crop(box)
		merge_img=Image.new('RGB',(96,96),0xFFFFFF)
		merge_img.paste(region,((96-im_1200_width)/2,0))
		merge_img.save(filename,quality=100)
		#region.save(filename,quality=100)
	print merge_img
	#im.close()
	return filename

def read_from_excel(file_name, sheet_name, row_count,row_number):
	data=xlrd.open_workbook(file_name)
	table=data.sheet_by_name(sheet_name)
	#wb=copy(data)
	#ws=wb.get_sheet(3)
	#print range(1,row_count+1)
	#for i in range(1,row_count+1):
	name_cn=table.cell(row_count,row_number).value
	#if (name_cn==''):
	return name_cn
		

def picture_transfer(picture_name):
	pic=open(picture_name,'rb')
	#print base64.b64encode(pic.read())
	return base64.b64encode(pic.read())
	#pic.close()

if __name__ == '__main__': 
	#file1=open('E:\\b1.txt','w')


	#read_from_excel('scholar_school.xls',u'Scholars',2)

	#picture_transfer(pic_name)
	#print url
	image='zdc.bmp'


	pic_name=make_post_thumb(image)
	print pic_name
	FF=picture_transfer(pic_name)
	print FF
	file1=open('E:\\'+image[:-4],'w')
	file1.write(FF)
	file1.close()
	print pic_name
	#os.remove(pic_name)
	has_photo=1



