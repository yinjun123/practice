#coding=utf-8
import json

from django.shortcuts import render
from django.template import RequestContext, loader
from .models import CartInfo, GoodDetailInfo
from goods.models import *
from django.http import HttpResponse, JsonResponse
from tiantianshengxian.derector import login_required

@login_required
def cartInfo(request):
    user = request.userinfo
    cartinfo = user.cartinfo_set.all()
    gooddetail = cartinfo[0].gooddetailinfo_set.all()
    #gooddetail = GoodDetailInfo.objects.all() #购物车商品详情（title...）
    #cartinfo = CartInfo.objects.all()   #用户购物车详情
    context = {'gooddetail':gooddetail, 'cartinfo':cartinfo}
    return render (request, 'cart/cart.html', context)

def addCart(request):   #添加到购物车
    gid = request.POST.get('gid')
    goodCount = request.POST.get('goodCount', 1)
    print(gid, goodCount)
    user = request.userinfo
    num = 0 # 购物车里面已有的商品数量

    if user:
        if not user.cartinfo_set.all():   #  如果用户没有购物车
            cart = CartInfo()
            cart.user = user
            cart.save()
        # 有购物车了  开始添加商品
        user_cartinfo = user.cartinfo_set.all()[0]
        user_cartinfo.count += int(goodCount)
        user_cartinfo.save()

        isnewgoods = True
        oldgooddetail = ''  #如果新添加大的商品在购物车内，就把gooddetail赋值给oldgooddetail
        
        for gooddetail in user_cartinfo.gooddetailinfo_set.all():
            num += 1
            if gooddetail.goods.id == int(gid):
                oldgooddetail = gooddetail
                isnewgoods = False
        
        if isnewgoods:  #如果是新的商品，创建新的gooddetailinfo对象
            print('new')
            gooddetailinfo = GoodDetailInfo()
            gooddetailinfo.goods_id = gid
            gooddetailinfo.cart_good = user_cartinfo
            gooddetailinfo.goodCount = goodCount
            gooddetailinfo.save()
            num += 1
        else:   #在购物车里有，更新购物车
            print('old')
            oldgooddetail.goodCount += int(goodCount)
            oldgooddetail.save()
    return  HttpResponse(num)

@login_required
def delGoodsDetail(request):   #删除购物车的商品
    idList = request.POST.get('id') #从html传来GoodDetailInfo对象的id
    user = request.userinfo
    cartInfo = user.cartinfo_set.all()[0]
    resp = {'status': 0, 'data': '无效参数'}
    for id in json.loads(idList):
        try:
            if not id:
                return JsonResponse(resp, safe=False)
            id = int(id)
        except ValueError:
            resp = {'status': 0, 'data': '无效参数'}
        else:
            goodDetail = GoodDetailInfo.objects.filter(pk=id)
            print(cartInfo.gooddetailinfo_set.all())
            print(goodDetail[0])
            if goodDetail and goodDetail[0] in cartInfo.gooddetailinfo_set.all():
                goodDetail.delete()
                resp = {'status': 1, 'data': '删除成功'}
            else:
                resp = {'status': 0, 'data': '购物车中不存在该商品或已删除'}
    return JsonResponse(resp, safe=False)

@login_required
def changeCount(request):    #‘+’键（添加商品数量）
    gid = request.POST.get('gid', 1)
    temp = request.POST.get('temp') #获取商品信息
    user = request.userinfo
    # msg = '什么都没加减'
    resp = {'status': 0, 'data': '操作失败'}
    try:
        temp = int(temp)
        if temp < 0:
            raise ValueError
    except ValueError:
        resp = {'status': 0, 'data': '{0}不是有效的整数'.format(temp)}
    else:
        for gooddetail in user.cartinfo_set.all()[0].gooddetailinfo_set.all():   #购物车商品
            if gooddetail.goods.id == int(gid):
                gooddetail.goodCount = temp
                resp = {'status': 1, 'data':  gooddetail.goodCount}
            gooddetail.save()
    return JsonResponse(resp, safe=False)
    # else:
    #     def cartCookie(request):
    #         response = HttpResponse()
    #         if request.COOKIES.has_key('gid'==gid):
    #             response.write(request.COOKIES['gid'])
    #         response.set_cookie('gid', gid, 120)
    #         response.set_cookie('goodcount', goodcount, None)


