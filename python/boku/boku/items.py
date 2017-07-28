# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BokuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #来源网站
    LYurl = scrapy.Field()
    #书名
    name = scrapy.Field()
    #价格
    jiage = scrapy.Field()
    #出版社
    ChuBanse = scrapy.Field()
    #ISBN号
    ISBN = scrapy.Field()
    #作者
    zuozhe = scrapy.Field()
    #页数
    yeshu = scrapy.Field()
    #出版时间
    CBshijian = scrapy.Field()
    #印刷时间
    YSshijian = scrapy.Field()
    #包装
    baozhuang = scrapy.Field()
    #开本
    kaiben = scrapy.Field()
    #版次
    banci = scrapy.Field()
    #印次
    yinci = scrapy.Field()
    #字数
    zhishu = scrapy.Field()
    #小图url
    xiaotuURL = scrapy.Field()
    #大图本地路径
    daimage = scrapy.Field()
    #小图本地路径
    xiaoimage = scrapy.Field()
    #大图url
    datuURL = scrapy.Field()
    #目录
    mulu = scrapy.Field()
    #内容提要
    LRtiyao = scrapy.Field()
    #书籍分类
    Bookfenlei = scrapy.Field()
    #入库时间
    RKSJ = scrapy.Field()

