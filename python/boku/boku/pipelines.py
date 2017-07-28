# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# from scrapy.pipelines.images import ImagesPipeline
# from scrapy.exceptions import DropItem
# from scrapy.http import Request
# class ImagePipeline(ImagesPipeline):
# 	def get_media_requests(self,item,info):
# 		for imageurl in item['datuURL']:
# 			yield Request(imageurl)
# 		for ximageurl in item['xiaotuURL']:
# 			yield Request(ximageurl)
# 	# def item_completed(self,results,item,info):
# 	# 	image_paths = [x['path'] for ok,x in results if ok]
# 	# 	if not image_paths:
# 	# 		raise DropItem("图片未下载好%s"%image_paths)
import requests
from boku import settings
import os
import MySQLdb
import datetime
import time
import hashlib
import sys

# from twisted.enterprise import adbapi

class ImagePipeline(object):

	def process_item(self,item,spider):
		daimages = []
		xiaoimages = []
		dir_path = '%s/%s'%(settings.IMAGES_STORE,spider.name)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		bgurl = item['datuURL']
		xurl = item['xiaotuURL']
		print xurl

		us = bgurl.split('/')[3:]
		us1 = xurl.split('/')[3:]
		image_name = '_'.join(us)
		image_name1 = '_'.join(us1)

		file_path = '%s/%s'%(dir_path,image_name)
		file_path1 = '%s/%s'%(dir_path,image_name1)
		daimages.append(file_path)
		xiaoimages.append(file_path1)
		if not os.path.exists(file_path):
			
			with open(file_path,'wb') as handle:
				response = requests.get(bgurl)
				for block in response.iter_content(1024):
					if not block:
						break
					handle.write(block)
				#print item['datuURL']
		if not os.path.exists(file_path1):
			
			with open(file_path1,'wb') as handle:
				response = requests.get(xurl)
				for block in response.iter_content(1024):
					if not block:
						break
					handle.write(block)
				#print item['datuURL']
		# for image_url2 in item['xiaotuURL']:
		# 	us = image_url2.split('/')[3:]
		# 	image_name = '_'.join(us)
		# 	file_path = '%s/%s'%(dir_path,image_name)
		# 	xiaoimages.append(file_path)
		# 	if os.path.exists(file_path):
		# 		continue
		# 	with open(file_path,'wb') as handle:
		# 		response = requests.get(image_url2)
		# 		for block in response.iter_content(1024):
		# 			if not block:
		# 		 		break
		# 			handle.write(block)
		# 		print item['xiaotuURL']
		item['daimage'] = daimages[0]
		item['xiaoimage'] = xiaoimages[0]
	 	
	


		mysqlcli = MySQLdb.connect(host = settings.MYSQL_HOST,user = settings.MYSQL_USER,passwd = settings.MYSQL_PASSWD,db = settings.MYSQL_DBNAME,port=settings.MYSQL_PORT,charset = "utf8")
		if item['ISBN'] !="":
			shijian = time.time()
			item['RKSJ'] = int(shijian)
			try:
				ISBN=item['ISBN']
				print type(item)

				m = hashlib.md5()
				m.update(ISBN)
				md5_str = m.hexdigest()
				a = md5_str[:2]
				L_int = int(a,16)
				print L_int
				s =  L_int%10
				print s
				name = "book_uu"+ str(s)
				print name
				cur = mysqlcli.cursor()
				sql = "INSERT INTO "+name+"(book_name,book_price,book_author,book_isbn,book_press,book_page,book_Publication_date,book_print_time,book_pack,book_size,book_editon,book_version,book_number,book_dapicture,book_xiaopicture,book_directory,book_profile,book_class,book_source,book_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				items  = [item['name'],item['jiage'],item['zuozhe'],item['ISBN'],item['ChuBanse'],item['yeshu'],item['CBshijian'],item['YSshijian'],item['baozhuang'],item['kaiben'],item['yinci'],item['banci'],item['zhishu'],item['daimage'],item['xiaoimage'],item['mulu'],item['LRtiyao'],item['Bookfenlei'],item['LYurl'],item['RKSJ']]
				for i in items:
					print i
				cur.execute(sql,items)
				mysqlcli.commit()
				cur.close()
			except MySQLdb.Error,e:
				print e
		else:
			print '无ISDN号！不保存'
		

# if __name__ == '__main__':
# 	a = ImagePipeline()
# 	a.MYSQL(item)