# coding=utf-8
import hashlib
import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.cache import cache

from users.models import UserInfo
from goods.models import GoodsInfo
from .models import OrderInfo, OrderDetailInfo
from cart.models import GoodDetailInfo
from tiantianshengxian.derector import login_required


_TRANSIT = 12   # 邮费
# 返回确认订单的页面，数据由js请求
@login_required
def place_order(request):
    user = request.userinfo
    auth_code = request.GET.get('authCode')
    print(auth_code)
    if auth_code:
        cache_data = cache.get(auth_code)
        print(cache_data)
        if cache_data:
            if user.id == cache_data.get('uid'):
                items = cache_data.get('items')
                return render(request, 'order/place_order.html', {'items':items})

# 用户中心全部订单页，只返回页面，订单数据由js发起get请求获取
@login_required
def user_center_order(request):
    return render(request, 'order/user_center_order.html')

# 缓存确认订单的数据
# 将以post方法发送的包含所购商品的’id’和‘数量’的数据找出商品对象
# 并返回一个对应该用户的验证码(authCode)，并将该验证码作为键，将确认订单的信息存储在缓存中
@login_required
def confirm_order(request):
    user = request.userinfo
    confirm_items = []

    s1 = hashlib.sha1()
    s1.update(str(datetime.now()))  # 以当前时刻作为值生成sha1验证码
    auth_code = s1.hexdigest()

    items = request.POST.get('items')
    isCart = request.POST.get('isCart')
    items = json.loads(items)
    if isCart == '1':
        for id in items:
            gd = GoodDetailInfo.objects.filter(pk=int(id))
            if gd:
                confirm_items.append({'goods': gd[0].goods, 'count': gd[0].goodCount})
    else:
        for item in items:
            count = item.get('count', 1)
            gid = item.get('gid')
            print(count, gid)
            if gid:
                goods = GoodsInfo.objects.filter(pk=gid)
                if goods:
                    confirm_items.append({'goods': goods[0], 'count': count})
                else:
                    pass
            else:
                pass
    cache.set(auth_code, {'uid': user.id, 'items': confirm_items, 'isCart': isCart})
    return HttpResponse(auth_code)

# 提交订单
@login_required
def submit_order(request):
    user = request.userinfo
    auth_code = request.GET.get('authCode')
    if auth_code:
        cache_data = cache.get(auth_code)
        if cache_data:
            if user.id == cache_data.get('uid'):
                items = cache_data.get('items')
                isCart = cache_data.get('isCart')

                order = OrderInfo()
                order.user = user
                order.save()  # 先初始化订单
                for item in items:
                    order_detail = OrderDetailInfo()
                    order_detail.goods = item.get('goods')
                    order_detail.count = item.get('count')
                    order_detail.price = item.get('goods').gprice
                    order.ototal += int(order_detail.count) * order_detail.price  # 计算总价
                    order_detail.order = order
                    order_detail.save()
                order.ototal += _TRANSIT
                order.save()  # 保存总价
                cache.delete(auth_code)
    return HttpResponse(request)

# 取消订单
@login_required
def cancel_order(request, oid):
    user = request.userinfo  # 当前已登录的用户
    order = OrderInfo.objects.filter(pk=oid)    # 要删除的订单
    msg = ''    # 回显信息
    status = 0      # 回显信息状态码，0表示失败，1表示成功
    if not order:
        msg = '订单"{0}"不存在或已删除'.format(oid)
    else:
        if order[0] not in user.orderinfo_set.all():
            msg = '用户"{0}"无权处理订单"{1}"'.format(user.name.encode('utf-8'), oid)
        else:
            print(order[0].state)
            if order[0].state == '0':
                msg = '用户"{0}"订单"{1}"退货成功，正在申请退款'.format(user.name.encode('utf-8'), oid)
                order[0].state = '2'
                status = 1
            elif order[0].state == '1':
                msg = '用户"{0}"取消订单"{1}"成功'.format(user.name.encode('utf-8'), oid)
                order[0].state = '2'
                status = 1
            elif order[0].state == '2':
                msg = '用户"{0}"删除订单"{1}"成功'.format(user.name.encode('utf-8'), oid)
                order[0].state = '3'
                order[0].isDelete = True
                status = 1
            else:
                msg = '无效操作'
            order[0].save()
        if status == 0:
            messages.error(request, msg)     # 无效操作，返回错误信息
        else:
            messages.success(request, msg)     # 操作成功，返回提示信息
    return redirect('users:manage-orders')

# 获取用户的全部订单信息
def get_order(request):
    page = int(request.GET.get('page', 1))    # 获取请页的页面，默认第一页
    user = request.userinfo  # 当前已登录的用户
    if user:
        orders = user.orderinfo_set.all().order_by('state', '-createdTime')    # 获取改用户的所有订单
        p = Paginator(orders, 3)    # 分页信息，每页显示3条
        if page > p.num_pages:
            page = p.num_pages
        data = p.page(page)
        return render(request, 'order/all_order.html', {'orders': data, 'page_count':p.num_pages, 'page_index': page, 'transit':_TRANSIT})

# 获取订单各件商品详细信息
def get_order_detail(request, oid):
    order_details = OrderDetailInfo.objects.filter(order__pk=oid)
    return HttpResponse(order_details)

