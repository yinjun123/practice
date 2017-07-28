# coding=utf-8

from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^place/$', place_order, name='place_order'),    # 显示确认订单页面
    url(r'^confirm/$', confirm_order, name='confirm_order'),    # 缓存确认订单数据
    url(r'^submit/$', submit_order, name='submit_order'),  # 提交订单，传入购物车的ID值
    url(r'^cancel/(?P<oid>\d+)/$', cancel_order, name='cancel_order'),  # 取消订单或删除
    url(r'^get_order/$', get_order, name='get_order'),    # 获取订单，传入订单表的ID值
    url(r'^get_order/(?P<oid>\d+)/$', get_order_detail, name='get_order_detail'),    # 获取订单详单，传入订单详情表的ID值
]