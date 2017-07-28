from django.shortcuts import render

from goods.models import TypeInfo, GoodsInfo
# Create your views here.

def index(request):
    types = TypeInfo.objects.all()
    user = request.userinfo
    cartGoodsCount = 0
    if user:
        cartGoodsCount = len(user.cartinfo_set.all()[0].gooddetailinfo_set.all())
        if not cartGoodsCount:
            cartGoodsCount = 0

    typeAndGoods = []
    for t in types:
        typeAndGoods.append([t,t.goodsinfo_set.all()[0:4]])

    context = {'types': types,
               'cartGoodsCount': cartGoodsCount,
               'typeAndGoods': typeAndGoods
               }
    return render(request, 'website/index.html', context)