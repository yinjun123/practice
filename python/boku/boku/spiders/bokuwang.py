# -*- coding: utf-8 -*-
import scrapy
from boku.items import BokuItem
import re
import sys
import time
import json
import hashlib
import MySQLdb
from boku import settings
reload(sys)
sys.setdefaultencoding("utf-8")

class BokuwangSpider(scrapy.Spider):
    r = re.compile(r"\d")
    name = "bokuwang"
    allowed_domains = ["bookuu.com"]
    num = 1000032
    url = "http://detail.bookuu.com/"
    html = ".html"
    start_urls = [url+str(num)+html]
    def parse(self, response):
        
    	item = BokuItem()
        #isbn

        ISB = response.xpath('//div[@class="parameter"]/ul/li[2]/span/text()').extract()

        if len(ISB) ==0:
            item['ISBN'] = ""
        else:
            # mysqlcli = MySQLdb.connect(host = "127.0.0.1",user = "root",passwd = "mysql",db = "Bookuu",port=3306,charset = "utf8")
            # print 6666666666
            # print mysqlcli
            # print 99999999999
            # m = hashlib.md5()
            # m.update(ISB[0])
            # md5_str = m.hexdigest()
            # a = md5_str[:2]
            # L_int = int(a,16)
            # s =  L_int%10
            # name = "book_uu"+ str(3)
            # # isbn_list = re.findall(r'\d',ISB[0])
            # # #数组转换成一个字符串
            # # isbn_str = ''.join(isbn_list)
            # # lens=len(isbn_str)
            # # if lens>8:
            # #     isbn_str = isbn_str[0:8]
            # # elif lens >0 and lens <8:
            # #     isbn_str = isbn_str[0:4]
            # # else:
            # #     return 'back'
            # # int_isbn = int(isbn_str)
            # # num =str(int(int_isbn % 10))
            # # table_name = 'bi_book'+num
            # cur = mysqlcli.cursor()
            # print "456789"
            # print name
            # ISB = str(ISB[0])
            # print type(ISB)
            # sql = "select * from "+name+" where book_isbn = '730704983X'"
            # print sql
            # cur.execute(sql)
            
            # result = cur.fetchone()
            # print "123456"
            # print result

            # #count = result['count(*)']
            # #print count
            # mysqlcli.commit()
            # cur.close()
            # #print result
            # #print "1111111111111111111"
            # # if result ==ISB[0]:

            item['ISBN'] = ISB[0]

    	item['LYurl'] = response.url
    	print response.url

    	
    	#书名
    	names =response.xpath('//div[@class="summary"]/div/h2/text()').extract()
    	if len(names)==0:
    		item['name'] = ""
    	else:
            item['name'] = names[0]
            #print type(item['name'])
           
        
    	#分类
        FL = response.xpath('//div[@class="breadcrumb"]/a/text()').extract()
        if FL ==[]:
        	item['Bookfenlei'] = ""
        else:
        	item['Bookfenlei'] = ",".join(FL)
        	#print item['Bookfenlei']
        #出版社
        CBS = response.xpath('//div[@class="parameter"]/ul/li[1]/a/text()').extract()
        if CBS ==[]:
        	item['ChuBanse'] =""
        else:
        	item['ChuBanse'] =CBS[0]
        	#print CBS

        #作者
        ZZ =response.xpath('//div[@class="parameter"]/ul/li[3]/a/text()').extract()
        if len(ZZ)==0:
        	item['zuozhe'] = ""
        else:
        	item['zuozhe'] = ZZ[0]
        	#print ZZ

        #价格
        a = response.xpath('//div[@class="sale"]/div[2]//span[@id="bk-d-pricing"]/text()').extract()
        if len(a)==0:
        	item['jiage'] = ""
        else:
        	item['jiage'] = a[0][1::]
        	#print a[0][1::]

        #页数
        yeshu = response.xpath('//div[@class="parameter"]/ul/li[4]/text()').extract()
        if len(yeshu) == 0:
        	item['yeshu'] =""
        else:
        	item['yeshu'] = yeshu[0][3::]
        	#print yeshu

        #出版时间
        CBSJ = response.xpath('//div[@class="parameter"]/ul/li[5]/text()').extract()
        if len(CBSJ) == 0:
        	item['CBshijian'] =""
        else:
            cbsj = CBSJ[0][5::]
            sj = time.strptime(cbsj,"%Y-%m-%d")
            CBSJ = int(time.mktime(sj))
            item['CBshijian'] = CBSJ
            #print CBSJ

        #印刷时间
        YSSJ = response.xpath('//div[@class="parameter"]/ul/li[6]/text()').extract()
        if len(YSSJ) == 0:
        	item['YSshijian'] =""
        else:
            yssj = YSSJ[0][5::]
            sj = time.strptime(yssj,"%Y-%m-%d")
            YSSJ = int(time.mktime(sj))
            item['YSshijian'] = YSSJ
            #print YSSJ
        #包装
        BZ = response.xpath('//div[@class="parameter"]/ul/li[7]/text()').extract()
        if len(BZ) ==0:
        	item['baozhuang'] = ""
        else:
        	item['baozhuang'] =BZ[0][3::]
        	#print type(item['baozhuang'])
        
        #开数
        KS = response.xpath('//div[@class="parameter"]/ul/li[8]/text()').extract()
        #patter = re.compile(r'\d+')
        #ks = patter.search(KS).group()
        if len(KS) ==0:
        	item['kaiben'] =""
        else:
        	item['kaiben'] = KS[0][3::]
        	#print type(KS[0])
        #版次
        BC = response.xpath('//div[@class="parameter"]/ul/li[9]/text()').extract()
        if len(BC) ==0:
        	item['banci'] =""
        else:
        	item['banci'] =BC[0][3::]
        	#print BC

        #印次
        YC = response.xpath('//div[@class="parameter"]/ul/li[10]/text()').extract()
        if len(YC) ==0:
        	item['yinci'] =""

        else:
        	item['yinci'] = YC[0][3::]
        	#print YC
        #字数
        ZS = response.xpath('//div[@class="parameter"]/ul/li[11]/text()').extract()
        if len(ZS) ==0:
        	item['zhishu'] =""
        else:
        	item['zhishu'] = ZS[0][3::]
        	#print ZS
        #内容概要

        NRTY = response.xpath('//div[@class="txt-wrap"]/div[@id="J_wrap_2"]/div[@class="txt-bd"]').extract()
        if NRTY ==[]:
        	item['LRtiyao'] = ""
        else:
        	item['LRtiyao'] =NRTY[0]
        	#print NRTY[0]

        #目录
        ML =response.xpath('//div[@class="txt-wrap"]/div[@id="J_wrap_5"]//div[@id="ml_s"]').extract()
        if ML ==[]:
        	item['mulu'] = ''
        else:
            item['mulu'] = ML[0]
            # print item['mulu']
            # # print json.dumps(ML)
            # print "1111111111111111111111111111111"

        #大图url

        datuurl = response.xpath('//div[@class="show-pic"]/div/a/img/@src').extract()
        if len(datuurl) ==0:
        	item['datuURL'] = ""
        	item['xiaotuURL'] = ""

        else:
        	item['datuURL'] = datuurl[0]
        	a = datuurl[0][0:-5]
        	item['xiaotuURL'] = a + "s.jpg"
        	#print datuurl
        	#print item['xiaotuURL']

        yield item
        self.num += 1
        while self.num <= 4000000:
        	
        	try:
        		yield scrapy.Request(self.url +str(self.num)+self.html,callback = self.parse,dont_filter=True)

        	except BaseException as re:
        		print "123456789"
    			self.num+=1
                continue