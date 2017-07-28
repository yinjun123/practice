#coding=utf-8
from django.shortcuts import render
from django.core.paginator import *
from django.http import HttpResponse

from models import *

 
def goodsInfo(request,css,name):
	user = request.userinfo
	cartGoodsCount = 0
	if user:
		cartGoodsCount = len(user.cartinfo_set.all()[0].gooddetailinfo_set.all())
		if not cartGoodsCount:
			cartGoodsCount = 0
	type_all = TypeInfo.objects.all()
	goods = GoodsInfo.objects.filter(gtitle=name)
	if goods:
		goodss = goods[0]
	else:
		goodss = []
	type_goods = type_all.filter(cssClass=css)
	list=GoodsInfo.objects.filter(gtype_id=type_goods[0].id,)
	a = list.order_by("-id")
	aa = a[0:2]
	context = {'goods':goodss,'a':aa,'type_all':type_all,"cssclass":css,'cartGoodsCount':cartGoodsCount}
	return render(request,'goods/goods.html', context)
	
def goodsList(request,css):
	num = request.GET.get('num',1)
	print (num)
	num1 = int(num)
	print num1
	order = request.GET.get('order',"id")
	print order 
	type_all = TypeInfo.objects.all()
	type_goods = type_all.filter(cssClass=css)
	if order == 'id':
		active = 'active'
		active1 = 'a'
		active2 = 'a'
	elif order == 'gprice':
		active = 'a'
		active1 = 'active'
		active2 = 'a'	
	elif order == 'gclick':
		active = 'a'
		active1 = 'a'
		active2 = 'active'

	user = request.userinfo
	cartGoodsCount = 0
	if user:
		cartGoodsCount = len(user.cartinfo_set.all()[0].gooddetailinfo_set.all())
		if not cartGoodsCount:
			cartGoodsCount = 0
		
	list=GoodsInfo.objects.filter(gtype_id=type_goods[0].id)
	orders = list.order_by(order)
	a = list.order_by("-id")
	
	paginator=Paginator(orders,10)
	page=paginator.page(int(num))
	context = {'page':page,
			   'a':a[0:2],
			   'type_all':type_all,
			   'page':page,
			   "cssclass":css,
			   "type_goods":type_goods[0],
			   "order":order,
			   'active':active,
			   'active1':active1,
			   'active2':active2,
			   'cartGoodsCount':cartGoodsCount,
			   'num1':num1
			   }
	return render(request,'goods/goodslist.html', context)



def get_goods(request):
	gid = request.GET.get('gid', None)
	code = 0    # 默认0, 0= 错误， 1=成功
	data = ''
	if gid:
		goods = GoodsInfo.objects.filter(pk=gid)
		print(goods)
		print(goods[0].gprice)
		if goods:
			code = 1  # 代表成功
			data = goods[0]
		else:
			code = 0
			data = '未找到有效商品'.encode('utf-8')
	else:
		code = 0
		data = '未提供参数"gid"'.encode('utf-8')
	resp_data = {'code':code, 'data': data}
	return HttpResponse(resp_data)