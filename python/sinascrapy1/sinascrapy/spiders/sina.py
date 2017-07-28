# -*- coding: utf-8 -*-
import scrapy
from sinascrapy.items import SinaItem
import os


class SinaSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://news.sina.com.cn/guide/"
    ]

    def parse(self, response):
    	items = []
    	#所有大类的标题和url
    	parentTitle = response.xpath('//div[@class="clearfix"]/h3/a/text()').extract()
    	parentUrls = response.xpath('//div[@class="clearfix"]/h3/a/@href').extract()
        #所有小类的标题和url
    	subUrls = response.xpath('//div[@id="tab01"]/div/ul/li/a/@href').extract()
    	subTitle = response.xpath('//div[@id="tab01"]/div/ul/li/a/text()').extract()
    
        #爬取所有大类
        for i in range(0, len(parentTitle)):
            # 指定大类目录的路径和目录名
            parentFilename = "./Data/" + parentTitle[i]

            #如果目录不存在，则创建目录
            if(not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            # 爬取所有小类
            for j in range(0, len(subUrls)):
                item = SinaItem()

                # 保存大类的title和urls
                item['parentTitle'] = parentTitle[i]
                item['parentUrls'] = parentUrls[i]

                # 检查小类的url是否以同类别大类url开头，如果是返回True (sports.sina.com.cn 和 sports.sina.com.cn/nba)
                if_belong = subUrls[j].startswith(item['parentUrls'])

                # 如果属于本大类，将存储目录放在本大类目录下
                if(if_belong):
                    subFilename =parentFilename + '/'+ subTitle[j]
                    # 如果目录不存在，则创建目录
                    if(not os.path.exists(subFilename)):
                        os.makedirs(subFilename)

                    # 存储 小类url、title和filename字段数据
                    item['subUrls'] = subUrls[j]
                    item['subTitle'] =subTitle[j]
                    item['subFilename'] = subFilename

                    items.append(item)

        for item in items:
        	yield scrapy.Request(url = item["subUrls"], meta={'meta_1' : item},callback=self.second_parse)
    def second_parse(self, response):
    	meta_1 = response.meta['meta_1']

    	sonUrls = response.xpath("//a/@href").extract()
            		
    	items = []
    	for i in range(0, len(sonUrls)):
    		if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])

    		if(if_belong):
    			item = SinaItem()
    			item['parentTitle'] = meta_1['parentTitle']
    			item['parentUrls'] = meta_1['parentUrls']
    			item['subTitle'] = meta_1['subTitle']
    			item['subUrls'] = meta_1['subUrls']
    			item['subFilename'] = meta_1['subFilename']
    			item['sonUrls'] = sonUrls[i]
    			items.append(item)
    	for item in items:
    		yield scrapy.Request(url=item['sonUrls'], meta={'meta_2':item},callback = self.detail_parse)
    def detail_parse(self, response):
    	item = response.meta['meta_2']
    	content = ""
    	head = response.xpath('//h1[@id="artibodyTitle"]/text()')
    	content_list = response.xpath('//div[@id="artibody"]/p/text()').extract()
    	for content_one in content_list:
    		content += content_one
    	item["head"] = head
    	item["content"] = content

    	yield item