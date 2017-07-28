# coding=utf-8
from django.conf.urls import url
import views
from order.views import user_center_order
urlpatterns = [

    #注册
    url(r'^register/$',views.register, name='register'),
    #检验用户名是否存在
    url(r'^checkname(.*)$',views.checkname, name='checkname'),
    #注册注册处理
    url(r'^registerHandle/$',views.registerHandle, name='registerHandle'),
    url(r'^base/$',views.base),
    #登陆
    url(r'^login/$',views.logn, name='login'),
    #登录页处理
    url(r'^loginHandle/$',views.lognHandle, name='loginHandle'),
    #删除session
    url(r'^delsession/$',views.delsession, name='delsession'),
    #用户中心
    url(r'^manage/info/$',views.ucenterInfo, name='manage-info'),
    url(r'^manage/orders/$',user_center_order, name='manage-orders'),
    #收货地址
    url(r'^manage/address/$',views.ucenterSite, name='manage-address'),
    #处理收货地址
    url(r'^addressHandle/$',views.addressHandle, name='addressHandle'),
    # url(r'^memory(.*)/$',views.memory)
]

