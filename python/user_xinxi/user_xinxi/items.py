# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserXinxiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #id
    user_id = scrapy.Field()
    #姓名
    name = scrapy.Field()
    #电话
    phone = scrapy.Field()
    #身份证号
    id_card = scrapy.Field()
    #银行卡号
    bank_number = scrapy.Field()
    #用户来源
    source = scrapy.Field()
    #app 版本
    app_version = scrapy.Field()
    #注册时间
    Registration_time = scrapy.Field()
    #申请数
    Application_number = scrapy.Field()
    #申请成功数
    successful_number = scrapy.Field()
    #标签
    label = scrapy.Field()
    #申请表id
    p_user_id = scrapy.Field()
    #申请贷款时间
    Application_time = scrapy.Field()
    #订单号
    order_number= scrapy.Field()
    #申请产品
    product= scrapy.Field()
    #结果
    result = scrapy.Field()
    #逾期天数
    overdue_situation = scrapy.Field()
    #备注
    note = scrapy.Field()
