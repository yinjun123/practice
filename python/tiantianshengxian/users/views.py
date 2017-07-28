#encoding=utf-8
from django.shortcuts import render,redirect
from models import *
from django.http import JsonResponse ,HttpResponse, HttpResponseRedirect
from hashlib import sha1
import json
from django.contrib import messages
from tiantianshengxian.derector import login_required
from cart.models import CartInfo

# Create your views here.
#跳到注册页
def register(request):
    return render(request,'users/register.html')
#加密
def shaOne(spwd):
    s1 = sha1()
    s1.update(spwd)
    sha1pwd = s1.hexdigest()
    return sha1pwd
#====================注册===========================

#失去焦点时判断用户名是否存在
def checkname(request,name):
    allUser = UserInfo.objects.all()
    # print (request)
    for temp in allUser:
        if name == temp.name:
            return JsonResponse({'data':'用户名已存在'})
    return JsonResponse({'data':'ok'})


#提交后验证数据是否完整
def registerHandle(request):
    uname = request.POST['name']
    upwd = request.POST['pwd']
    email = request.POST['email']
    if uname == '' or upwd == '' or email == '':
        msg = "信息未填写完整"
        messages.error(request, msg)
        return render(request,'users/register.html')
    #check未勾选不传递数据，长度变成4
    l = len(request.POST)
    if l == 5:
        #保存到数据库
        #加密
        upwd = shaOne(upwd)
        #添加到数据库
        newUser = UserInfo()
        # print(type(uname.encode('utf-8')))
        newUser.name = uname.encode('utf-8')
        newUser.pwd = upwd
        newUser.email = email
        newUser.save()
    #创建购物车对象
        newCart = CartInfo()
        newCart.user = newUser
        newCart.save()

        msg = '恭喜你，注册成功，请先登陆'
        messages.success(request, msg)
        return HttpResponseRedirect('/users/login/')
    else:
        msg = '亲，请同意用户协议'
        messages.error(request, msg)
        return HttpResponseRedirect('/users/register/')
#=================================登陆=======================================
#==查看_base页
def base(request):
    return render(request,'_base.html')
#登录页
def logn(request):
    return  render(request,'users/login.html')
#处理提交数据
def lognHandle(request):
    username=request.POST['username']
    userpwd =request.POST['pwd']
    allUser = UserInfo.objects.all()
    for temp in allUser:
        if temp.name == username:
            u = UserInfo.objects.filter(name=username)
            print (u)
            #获取对象是一个列表，提取第0个
            pwd = u[0].pwd
            userpwd = shaOne(userpwd)
            if userpwd == pwd:
                userId = u[0].id
                context = {'id':userId}
                #写入session
                request.session['uid'] = userId
    #关闭浏览器时，删除session
                request.session.set_expiry(0)
                #登陆成功后，跳转到首页
                return HttpResponseRedirect('/')
            else:
                msg = '密码错误，请重新登陆'
                messages.error(request, msg)
                return HttpResponseRedirect('/users/login/')
#================没遍历到用户
    msg = '用户名错误'
    messages.error(request, msg)
    return HttpResponseRedirect('/users/login/')
#删除session
@login_required
def delsession(request):
    request.session.flush()
    # del request.session['uid']
    return HttpResponseRedirect('/')

#===============================用户中心======个人信息=========================
@login_required
def ucenterInfo(request):
    u = request.userinfo
    context = {'user':u}
    return render(request, 'users/ucenterInfo.html',context)
#===============================用户中心======收货地址=========================
@login_required
def ucenterSite(request):
    return render(request, 'users/ucenterSite.html')

# #===处理修改地址===
# def addressHandle(request):
#     u = request.userinfo
#     s = request.POST['sendee']
#     a = request.POST['address']
#     c = request.POST['code']
#     n = request.POST['number']
#     print(u)
#     if s and a and n:
#         u.sendee = s
#         u.address = a
#         u.code = c
#         u.phoneNumber = n
#         u.save()
#         return HttpResponseRedirect('/users/manage/address/')
#     else:
#         msg = '未完成修改，请将信息填写完整'
#         messages.error(request, msg)
#         return render(request, 'users/ucenterSite.html')

#===处理修改地址===
def addressHandle(request):
    user = request.userinfo
    sendee = request.POST['sendee']
    address = request.POST['address']
    code = request.POST['code']
    phoneNumber = request.POST['number']

    if sendee and address and phoneNumber:
        user.sendee = sendee
        user.address = address
        user.code = code
        user.phoneNumber = phoneNumber
        addr = '{0}({1} 收){2}'.format(address.encode('utf-8'), sendee.encode('utf-8'), phoneNumber.encode('utf-8'))
        addrs = user.addrs
        if addrs:
            newAddr = json.loads(addrs)
            newAddr.append(addr)
        else:
            newAddr = [addr]
            user.defaultAddr = 0
        user.addrs = json.dumps(newAddr)
        user.save()
        return HttpResponseRedirect('/users/manage/address/')
    else:
        msg = '未完成修改，请将信息填写完整'
        messages.error(request, msg)
        return render(request,'users/ucenterSite.html')


