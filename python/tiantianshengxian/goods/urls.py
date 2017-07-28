# coding=utf-8

from django.conf.urls import url
import views

urlpatterns = [
    #url(r'^gprice/$', views.gprice),
    url(r'^(?P<css>[a-z]+)/$', views.goodsList,name="goodsList"),
    #url(r'^list/(\d*)/([a-z]*)/$', views.goodsList),

    url(r'^(?P<css>[a-z]+)/(?P<name>.*?)/$',views.goodsInfo,name="goodsInfo"),
    url(r'^get_goods/$', views.get_goods, name='get')
]