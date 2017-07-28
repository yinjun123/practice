#coding=utf-8
from __future__ import unicode_literals

from django.db import models

class TypeInfo(models.Model):
	title = models.CharField('商品分类',max_length=20)  #商品类别名称
	isDelete = models.BooleanField(default=False)   #是否有此类
	cssClass = models.CharField('商品名称', max_length=20)  #商品名称
	img_path = models.CharField('商品分类图片', max_length=127) # 商品分类图片
	class Meta():
		db_table='typeinfo'
	def __str__(self):
		return self.title.encode('utf-8')


class GoodsInfo(models.Model):
	gtitle = models.CharField('商品名称',max_length=20)   #商品名称
	gprice = models.DecimalField('商品价格',max_digits=7,decimal_places=2)  #商品价格
	gdesc = models.TextField('商品描述')  #商品描述
	ginfo = models.CharField('商品简介',max_length=100, default=' ')  #商品简介
	gpath = models.CharField('list路径',max_length=1000)  #商品图片路径
	gdetail = models.CharField('detail路径',max_length=1000,default=' ')  #detail图片路径
	gunit = models.CharField('商品单位',max_length=100)   #商品单位
	gcount = models.IntegerField('商品库存',default=1000)  #商品库存
	gclick = models.IntegerField('商品点击量',default=0)   #点击量
	gtype = models.ForeignKey('TypeInfo')   #外键
	isDelete = models.BooleanField(default=False)
	class Meta():
		db_table='goodsinfo'
	def __str__(self):
		return self.gtitle.encode('utf-8')



