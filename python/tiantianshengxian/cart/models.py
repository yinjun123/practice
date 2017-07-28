#coding:utf-8
from __future__ import unicode_literals
from django.db import models
from users.models import UserInfo
from goods.models import GoodsInfo

class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo)   #获取用户信息
    count = models.IntegerField('数量', default=0)  #总商品件数
    class Meta:
        db_table = 'cartinfo'
    def __str__(self):
        return self.user.name.encode('utf-8')

class GoodDetailInfo(models.Model):
    goods = models.ForeignKey(GoodsInfo)  #用户页商品详情
    cart_good = models.ForeignKey('CartInfo')   #购物车商品
    goodCount = models.IntegerField('数量', default=0)  #单件商品数量
    total = models.DecimalField('小计',max_digits=7,decimal_places=2)
    class Meta:
        db_table = 'gooddetailinfo'
    def __str__(self):
        return self.goods.gtitle.encode('utf-8')

    @property
    def total(self):
        total = self.goodCount*self.goods.gprice
        return total
  
    def name(self):
        return self.goods.gname
  
    def price(self):
        return self.goods.gprice
  
    def augmentGoodCount(self):
        self.goodCount += goodCount
        return self.goodCount

