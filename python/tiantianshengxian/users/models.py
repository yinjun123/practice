#coding=utf-8
from __future__ import unicode_literals
import json

from django.db import models

# Create your models here.
class UserInfo(models.Model):

    name = models.CharField('用户名',max_length=20)
    pwd = models.CharField('密码',max_length=40)
    isdelete = models.BooleanField('是否删除',default=False)
    address = models.CharField('地址',max_length=100)
    phoneNumber = models.CharField('联系方式',max_length=11)
    #邮编
    code =models.CharField('邮编',max_length=6)
    #邮箱
    email = models.CharField('邮箱',max_length=30)
    # 新增收件人
    sendee = models.CharField('收件人',max_length=20)
    def __unicode__(self):
        return u"%s"%self.name

    addrs = models.TextField(null=True, blank=True)
    defaultAddr = models.IntegerField(null=True, blank=True)

    @property
    def get_addrs(self):
        addrs = json.loads(self.addrs)
        item_addr = []
        for index in xrange(len(addrs)):
            item_addr.append([index, addrs[index]])
        return item_addr


