# coding=utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cartInfo/$', views.cartInfo, name="cartInfo"),
    url(r'^addCart/$', views.addCart),
    url(r'^delGoodsDetail/$', views.delGoodsDetail, name='delGoodsDetail'),
    url(r'^changeCount/$', views.changeCount),
]