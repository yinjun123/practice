from django.contrib import admin

from models import OrderInfo, OrderDetailInfo
# Register your models here.

class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'ototal', 'orderState', 'createdTime', 'payTime', 'isDelete']

class OrderDetailInfoAdmin(admin.ModelAdmin):
    list_display = ['order', 'goods', 'count', 'price']

admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(OrderDetailInfo, OrderDetailInfoAdmin)