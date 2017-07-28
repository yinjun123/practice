# coding=utf-8
import functools

from django.shortcuts import redirect

def login_required(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.userinfo:
            return redirect('users:login')
        return func(request,*args, **kwargs)
    return wrapper