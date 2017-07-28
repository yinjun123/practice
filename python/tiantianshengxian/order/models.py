# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime
from random import randint

from django.db import models

from users.models import UserInfo
from goods.models import GoodsInfo


# 订单模型
class OrderInfo(models.Model):

    id = models.CharField('订单编号', max_length=31, primary_key=True, null=False)    #订单编号
    user = models.ForeignKey(UserInfo)    # 订单拥有者
    ototal = models.DecimalField('总价', max_digits=7, decimal_places=2, default=0)    # 订单总金额
    state = models.CharField('订单状态', max_length=1, default='0')    # 订单状态（0:已删除,1:待付款,2:已取消,3:已付款）
    createdTime = models.DateTimeField('创建时间',auto_now_add=True)    # 订单生成时间
    address = models.CharField(max_length=127)   # 地址
    payTime = models.DateTimeField('支付时间',null=True, default=None)    # 支付时间
    payMethod = models.IntegerField(null=True,default=0)    # 支付方式
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = 'orderInfo'

    def save(self):
        if not self.id:
            now = datetime.now()
            # 自动生成订单编号
            self.id = '{0}{1:0>2}{2:0>2}{3:0>2}{4:0>2}{5:0>2}{6:0>6}'.format(
                now.year,now.month,now.day,now.hour,now.minute,now.second,randint(0,999999))
        super(OrderInfo, self).save()    # 最后调用父类save方法

    # 订单状态
    def orderState(self):
        ORDER_STATE = {'0': '待付款', '1': '已付款', '2': '已取消', '3': '已删除'}
        return ORDER_STATE[self.state]

    def get_pay_method(self):
        PAY_METHOD = {'0': '货到付款', '1': '微信支付', '2': '支付宝', '3': '银行卡支付'}
        return PAY_METHOD['%d'%self.payMethod]

    def __str__(self):
        return self.id.encode('utf-8')

#订单详情模型
class OrderDetailInfo(models.Model):

    order = models.ForeignKey(OrderInfo)    # 对应订单编号
    goods = models.ForeignKey(GoodsInfo)    # 订单商品列表
    count = models.IntegerField('数量')    # 订单商品数量
    price = models.DecimalField('价格', max_digits=7, decimal_places=2)    # 商品提交时的价格
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'orderDetailInfo'

    def __str__(self):
        return '{0}-{1}'.format(self.goods.gtitle, self.count).encode('utf-8')
