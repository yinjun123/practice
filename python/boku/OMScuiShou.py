# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
url = "http://oms.sdzz.la:8080/admin/overduecollection/getYuQiBorrowUserList"
response  = requests.get(url)
html = response.text
selector = etree.HTML(html)
overduelist = selector.xpath("//*[@id='searchForm']/table[2]/tbody")

for list in overduelist[1:]:
    time.sleep(1)
    # 姓名
    name = list.xpath("./tr/td[2]/text()")[0]
    print name
     #手机号
    phone = list.xpath("./tr/td[3]/text()")[0]
    print phone
    #身份证
    Id_card = list.cpath("./tr/td[4]/text()")[0]
    print Id_card
    #借款本金
    borrow_money = list.cpath("./tr/td[5]/text()")[0]
    print borrow_money
    #应还本金
    yinghuan_money = list.cpath("./tr/td[6]/text()")[0]
    print yinghuan_money
    #罚息金额
    faxi_money = list.cpath("./tr/td[7]/text()")[0]
    print faxi_money
    #以还金额
    yihuan_money = list.cpath("./tr/td[8]/text()")[0]
    print yihuan_money
    #逾期笔数
    overdue_number= list.cpath("./tr/td[9]/a/text()")[0]
    print overdue_number
    #当前逾期时长
    overdue_length = list.cpath("./tr/td[10]/text()")[0]
    print overdue_length
    #剩余未还总额
    weihuan_money = list.xpath("./tr/td[10]/text()")[0]
    print  weihuan_money
    #催收员

    odv = list.xpath("./tr/td[11]/text()")
    if odv ==[]:
        print "kong"
    else:
         print odv
    #预期类型
    overdue_type = list.xpath("./tr/td[12]/text()")[0]
    print overdue_type