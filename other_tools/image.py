#!/usr/bin/env python
#encoding=utf-8

import cStringIO, urllib2, Image
import xlrd
import base64
import pymongo
import json
from pymongo import Connection
import os

def read_online_image(url):
	url=url
	file1=urllib2.urlopen(url)
	tmpIm=cStringIO.StringIO(file1.read())
	return tmpIm
	#im=Image.open(tmpIm)

	#print im.format,im.size, im.mode


def make_post_thumb(path, size=(96,96)):
	#base,ext=os.path.splitext(path)
	try:
		im=Image.open(path)
	except IOError:
		print 'in IOError'
		return
	mode=im.mode
	if mode not in ('L','RGB'):
		if mode=='RGBA':
			im.load()
			alpha=im.split()[3]
			bgmask=alpha.point(lambda x:255-x)
			im=im.convert('RGB')
			im.paste((255,255,255), None, bgmask)
		else:
			im=im.convert('RGB')

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
	#print merge_img
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
	return base64.b64encode(pic.read())
	#pic.close()

if __name__ == '__main__': 


	#read_from_excel('scholar_school.xls',u'Scholars',2)

	#picture_transfer(pic_name)

	connection=Connection('10.77.20.50',27017)
	db=connection.Microsoft_AS
	collection=db.test4
	for i in range(1,4535):
		school=read_from_excel('scholar and school.xls',u'Scholars',i,0)
		name=read_from_excel('scholar and school.xls',u'Scholars',i,2)
		print name
		name_lowcase=name.lower()
		native_name=read_from_excel('scholar and school.xls',u'Scholars',i,1)
		homepage=read_from_excel('scholar and school.xls',u'Scholars',i,3)
		url=read_from_excel('scholar and school.xls',u'Scholars',i,4)
		photo=''
		if (url==''):
			photo=''
			has_photo=0
		else:
			try:

				#print url
				image=read_online_image(url)
				#print image
				pic_name=make_post_thumb(image)
				#print pic_name
				photo=picture_transfer(pic_name)
				#print photo
				os.remove(pic_name)
				has_photo=1
			except:
				print url
				photo=''
				has_photo=0


		if (school!=''):
			collection.insert({'DisplayPhotoURL':url, 'has_photo':has_photo, 
				'affiliation':school, 'ban':0,'email':'', 'homepage':homepage,
				'name':name,'name_low_case':name_lowcase, 'native_name':native_name,
				'photo':photo, 'scholar_id':i+54332692-1, 'insert_by':'LJ'})



		#collection.insert({'DisplayPhotoURL':123,'mmm':1234})







