#coding:utf-8
#上面设置的是py文件的编码
#自带的Tkinter模块
from Tkinter import *
from ScrolledText import ScrolledText
import urllib,requests,re
import threading
import time
#输出的内容编码是utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#用来存视频地址和名称
url_name=[]
#页码
a=1
def get():
    global a
    #加上User-Agent代理模拟浏览器请求
    user_agent={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    url='http://www.budejie.com/'+str(a)
    var.set('已经获取到第%s页'%(a))
    html = requests.get(url,headers=user_agent).text
    a+=1
    #正则匹配
    #.*？表示匹配任意字符但不取出来 (.*?)匹配任意字符但要取出来
    #re.S表示匹配换行符
    content=re.compile(r'(<div class="j-r-list-c">.*?</div>.*?</div>)',re.S)
    # print type(content)
    # sys.exit()
    #findall返回的是列表
    contents=re.findall(content,html)
    for i in contents:
        video_re = re.compile(r'data-mp4="(.*?)">',re.S)
        video_urls=re.findall(video_re, i)
        if video_urls:
            name=re.compile(r'<a href="/detail-.{8}?.html">(.*?)</a>',re.S)
            names=re.findall(name,i)
            #zip()就是合并列表的意思
            for i,k in zip(names,video_urls):
                url_name.append([i,k])
    #返回视频地址和名称
    return url_name
# url_name=get()
# print url_name
# sys.exit()
id=1#视频个数
def write():
    global id
    while id<30:
        #url_name视频地址和名称
        url_name=get()
        for i in url_name:
            print i[1]
            #urlretrieve()下载函数
            #name = './baishibudeqijie\\%s.mp4' % (i[0].decode('utf-8').encode('gbk'))


            times = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
            name = './video/'+times+'.mp4'
            print name
            urllib.urlretrieve(i[1],name)
            text.insert(END,str(id)+'.'+i[1]+'\n'+i[0]+'\n')
            #删除已经有的数据
            url_name.pop(0)
            id+=1
    var.set('已经抓取完毕！！！')
def start():
    th=threading.Thread(target=write)
    th.start()
    th.join()


#gui框
root = Tk()
root.title('视频多线程')
#窗口坐标和大小 +代表调整坐标 x代表调整大小
root.geometry('+200+100')
#滚动条
text = ScrolledText(root,font=('微软雅黑',10))
#实现滚动条方法grid()
text.grid()
#按钮
#command=start 按钮绑定方法
button = Button(root,text='开始爬取',font=('微软雅黑',10),command=start)
#实现按钮
button.grid()
#label
#文本变量
var=StringVar()
#textvariable 绑定文本变量
label = Label(root,font=('微软雅黑',10),fg='red',textvariable=var)
label.grid()
#文本变量文本内容
var.set('已准备...')
#实现窗口命令
root.mainloop()
