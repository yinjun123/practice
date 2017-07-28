# -*- coding: utf-8 -*-
import scrapy
import time

class UserSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['http://oms.sdzz.la:8080']
    #start_urls = ['http://http://oms.sdzz.la:8080/']

    def start_requests(self):#获得第一页
        url = 'http://oms.sdzz.la:8080/admin/user/getUserInfoList'
        d = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))
        yield scrapy.FromRequest(
            url = url,
            formdata = {"Content-Disposition: form-data; name='startDate'":d,
                        "Content-Disposition: form-data; name='endDate'":d,
                        "Content-Disposition: form-data; name='mobile'":"",
                        "Content-Disposition: form-data; name='channel'":"",
                        "Content-Disposition: form-data; name='pageNo'":"1",
                        "Content-Disposition: form-data; name='pageSize'":"500",
                        "Content-Disposition: form-data; name='lastUserId'":""},
            callback = self.parse_page
        )
    def parse_page(self,response):
        for i in res:

            response.xpath()#拿到页面的最后一个用户id
            if #判断借款次数如果是0不发送，如果不是0发送请求
                yield scrapy.Request(url, callback=self.shengqing)
            else：
                print "借款次数为0,不发送请求"
    def shenqing(self,response):
        #对爬取到的申请列进行循环

    def next_(self,pageid):
        #得到pageid,发送post请求得到下也数据






id = item['user_id']
id-500













