import urllib2

response = urllib2.urlopen("http://www.baidu.com")

html = response.read()



import urllib2

response = urllib2.urlopen("http://www.baidu.com")

html = response.read()

print html

python urllib2_urlopen.py

import urllib2

request = urllib2.Request("http://www.baidu.com")

response = urllib.urlopen(request)

html = response.read()

print html



import urllib2

url = "http://www.baidu.com"

headerss = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

request = urllib2.Request(url,headers = headerss)

response = urllib2.urlopen(request)

html = response.read()
response.code #可以查看响应状态码
print html 

import urllib2
import random
url = "http:www.baidu.com"
ua_list = [
	"Mozilla/5.0 (Windows NT 6.1; ) Apple.... ",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0)... ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X.... ",
    "Mozilla/5.0 (Macintosh; Intel Mac OS... "
]
user-Agent = random.choice(ua_list)
request = urllib2.Request(url)
request.add_header("User-Agent",user_agent)
request.get_header("User-agent")

response = urllib.urlopen(request)
html = response.read()
print html

import urllib

word = {"wd":"传智博客"}

urllib.urlencode(word)
"wd=%E4%BC%A0%E6%99%BA%E6%92%AD%E5%AE%A2"
print urllib.unquote("wd=%E4%BC%A0%E6%99%BA%E6%92%AD%E5%AE%A2")
wd=传智播客

import urllib
import urllib2

url = "http://www.baidu.com/s"

word = {"wd":"传智播客"}
word = urllib.urlencode(word)
newurl = url + "?" + word 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)}
request = urllib2.Request(newurl,headers = headers)
response = urllib2.urlopen(request)
html = response.read()
print html

if __name__ == "__main__"

	kw = raw_input("请输入贴吧名称：")
	beginPage = int(raw_input("请输入起始页"))
	endPage = int(raw_input("请输入终止页"))

	url = "http://tieba.baidu.com/f?"
	key = urllib.urlencode({"kw":kw})

	url = url + key
	tiebaSpider(url,beginPage,endPage)

def tiebaSpider(url,beginPage, endPage):
	
	for page in range(begInPage, endPage +1):
		pn = (page - 1) * 50
		filename = "第" + str(page) + "页.html"
		fullurl = url + "&pn=" +str(pn)
		html = loadPage(fullurl,filename)
		writeFile(html,filename)

def loadPage(url, filename):

	print "正在下载" + filename

	headers = {"User-Agent":"Mozilla"}
	request = urllib2.Request(url,headers = headers)
	response = urllib2.urlopen(request)
	return response.read()
def writeFile(html,filename):
	print  "正在存储" + filename
	with open(filename,'w') as f:
		f.write(html)
	print "-" *20


import urllib
import urllib2
url = "https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action"

headers = {
	"User-Agent": "Mozilla...."
}
formdata = {
	"start":"0",
	"limit":"10"

}
data = urllib.urlencode(formadata)
request = urllib2.Request(url,data = data ,headers = headers)
response = urllib2.urlopen(request)
print response.read()


import urllib
import urllib2
import ssl
context = ssl.create_unverified_context()
url = "https://www.12306.cn/mormhweb/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64;
request = urllib2.Request(url,headers=headers)
response = urllib2.urlopen(request)
print response.read()

import urllib2
http_handler = urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(http_handler)
request = urllib2.Request("http://www.baidu.com")
response = opener.open(request)
print response.read()

import urllib2

httoproxy_handler = urllib2.ProxyHandler({"http" : "124.88.67.81:80"})
nullpxoxy_handler = urllib.ProxyHandler({})
proxySwitch = True

if proxySwitch:
	opener = urllib2.build_opener(httoproxy_handler)
else:
	opener = urllib.build_opener(nullproxy_handler)

request = urllib2.Request("http://www.baidu.com")
response = opener.open(request)
print response.read()











#coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import torndb
import json
import torndb

class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db = torndb.Connection(
            host="127.0.0.1",
            database='itcast',
            user='root',
            password='mysql'
        )

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('itcast', 'python')
        self.set_header('name', 'moz')

    def prepare(self):
        if self.request.headers.get('Content-Type', "").startswith('application/json'):
            self.json_dict = json.loads(self.request.body)
        else:
            self.json_dict = None

class IndexHandler(BaseHandler):
    def get(self):
        self.write('index')
        self.set_header('name', 'mozaa')

    def post(self):
        title = self.get_argument('title')
        position = self.get_argument('position')
        price = self.get_argument('price')
        score = self.get_argument('score')
        comments = self.get_argument('comments')
        print title, position, price, score, comments

        sql = 'insert into houses(title, position, price, score, comments) values(%(title)s, %(position)s, %(price)s, %(score)s, %(comments)s)'
        try:
            house_id = self.application.db.execute(sql, title=title, position=position, price=price, score=score, comments=comments)
        except Exception as e:
            self.write('error db')
            print e
        else:
            self.write("house id:%s" % house_id)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    setting = {4545
        'debug': True,
    }
    app = Application(
        [
            (r'/', IndexHandler)
        ],
        **setting
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.current().start()