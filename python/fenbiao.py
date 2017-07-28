#-*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.utils import parseaddr,formataddr
import MySQLdb,time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def mysql_fenbiao():
	d = time.strftime('%Y-%m-%d',time.localtime(time.time()-86400))
	a = d+"%"
	# try:
	#链接本地数据库
	try:
		mysqlcli = MySQLdb.connect(host='120.92.74.189', user='root', passwd='Rf804dhu31vm6H9i4shg3j19kn65dQ',
								   db='spider_data', port=3306, charset="utf8")

		sql1 = "select overdue_days,name,phone,Booked_time from statements_list where Booked_time like '%s'"%a
		cur = mysqlcli.cursor()
		cur.execute(sql1)
		result = cur.fetchall()#将前一天的数据全部取出来，是一个2维元组

		f = open("test.txt","w+")
		f.close()
		for res in result:
			try:
				tianshu = res[0] 
				sql2 = "select count(*) from FB1 where phone = '%s' union select count(*) from FB2 where phone = '%s' union select count(*) from FB3 where phone = '%s'"%(res[2],res[2],res[2])
				cur.execute(sql2)#将3张表进行连接查询，有数据返回元组长度为1，无数据元组长度为2
				mysqlcli.commit()
				ress = cur.fetchall()
			except Exception,e:
				print u"数据库发生错误",e
			print len(ress)
			if len(ress) ==1:# 如果长度为1进行判断分表插入
				if tianshu<=3:#白名单
					try:
						sql = "INSERT INTO FB1 (id,name,phone,overdue_days) VALUES (%s,%s,%s,%s)"
						item = [res[2],res[1],res[2],res[0]]
						b =res[1]+'-'+ str(res[2]) +'-'+str(res[0])+'\r\n'
						print b
						a = cur.execute(sql,item)
						if a==1:
							print u"插入成功"
						mysqlcli.commit()
						f =  open("test.txt","a+")
						f.write(b)
						f.close()
						 
					except Exception,e:
						print u"数据库发生错误",e

				elif tianshu<=14 and tianshu>=4:#灰名单
					try:
						sql = "INSERT INTO FB2 (id,name,phone,overdue_days) VALUES (%s,%s,%s,%s)"
						item = [res[2],res[1],res[2],res[0]]
						print item
						a=cur.execute(sql,item)
						if a==1:
							print u"插入成功"
						mysqlcli.commit()
					except Exception,e:
						print "数据库发生错误",e
				elif tianshu>=15:#黑名单
					try:
						sql = "INSERT INTO FB3 (id,name,phone,overdue_days) VALUES (%s,%s,%s,%s)"
						item = [res[2],res[1],res[2],res[0]]
						
						a = cur.execute(sql,item)
						if a==1:
							print u"插入成功"
						mysqlcli.commit()
					except Exception,e:
						print "数据库发生错误",e
			else:
				print u"重复数据"
		cur.close()
		sendMail(' 请查收！', 'test.txt')
	except Exception,e:
		print u"数据库发生错误",e
#格式化邮件地址
def formatAddr(s):
	name, addr = parseaddr(s)
	return formataddr((Header(name, 'utf-8').encode(), addr))

def sendMail(body, attachment):
	smtp_server = 'smtp.qq.com'
	from_mail = '453712212@qq.com'#发信人账号
	mail_pass = 'dbcfigpftsrxbggh'
	to_mail = "yinjun453712212@163.com"#收信人账号
	# 构造一个MIMEMultipart对象代表邮件本身
	msg = MIMEMultipart()
	# Header对中文进行转码
	msg['From'] = formatAddr('殷俊 <%s>' % from_mail).encode()#发送人姓名，和邮箱
	msg['To'] = to_mail#收信人邮箱
	msg['Subject'] = Header('你好', 'utf-8').encode()#标题
	# plain代表纯文本
	msg.attach(MIMEText(body, 'plain', 'utf-8'))#正文内容以文本的
	# 二进制方式模式文件
	with open(attachment, 'rb') as f:
		# MIMEBase表示附件的对象
		mime = MIMEBase('text', 'txt', filename=attachment)
		# filename是显示附件名字
		mime.add_header('Content-Disposition', 'attachment', filename=attachment)
		# 获取附件内容
		mime.set_payload(f.read())
		encoders.encode_base64(mime)
		# 作为附件添加到邮件
		msg.attach(mime)
	try:
		s = smtplib.SMTP_SSL(smtp_server,465)#465是SMTP的
		s.login(from_mail, mail_pass)
		s.sendmail(from_mail, to_mail, msg.as_string())  # as_string()把MIMEText对象变成str
		s.quit()
	except smtplib.SMTPException as e:
		print "Error: %s" % e

if __name__=="__main__":
	mysql_fenbiao()
