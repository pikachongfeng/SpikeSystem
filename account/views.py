import logging

from django.http import HttpResponse,HttpResponseRedirect
#from django.views.generic import FormView, RedirectView
#from django.contrib.auth import authenticate, login, logout
from .models import User
from django.views.decorators.csrf import csrf_protect
from ratelimit.decorators import ratelimit
from django.shortcuts import render
from django.contrib.auth import authenticate,login

from .forms import LoginForm,RegisterForm

logger = logging.getLogger(__name__)

@csrf_protect #为当前函数强制设置防跨站请求伪造功能
@ratelimit(key='ip', rate='5/m',block=True) #限制每分钟只能登录5次，防止暴破
def Login(request): #登录函数，与urls.py里的对应
    #登录前的网页                                                     当HTTP_REFERER缺省时，返回空字符串
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        #从数据库中找出符合条件的用户
        user = authenticate(username = username,password = password)
        if user is not None and user.is_active:
            #调用django框架下login函数
            login(request,user)
            #匹配成功，跳转到index
            response = HttpResponseRedirect('/account/index/')
            #将username写入浏览器cookie,失效时间为3600
            response.set_cookie('username',username,3600)
            return response
        else:
            #匹配失败，重返登录界面
            return HttpResponseRedirect('/account/login/')
    else:
        lf = LoginForm()

    return render(request,'account/login.html',{'lf':lf})

def Register(request):
    if request.method == "POST":
        rf = RegisterForm(request.POST)
        if rf.is_valid():
            username = rf.cleaned_data['username']
            email = rf.cleaned_data['email']
            password = rf.cleaned_data['password2']
            #自动给密码hash
            User.objects.create_user(username = username, email = email, password = password)
            return HttpResponse(u'注册成功')
    else:
        rf = RegisterForm()
    return render(request,'account/regist.html',{'rf':rf})

def index(request):
    username = request.COOKIES.get('username','')
    return render(request,'account/index.html' ,{'username':username})

def logout(request):
    response = HttpResponse('logout!')
    #清理cookie里保存username
    response.delete_cookie('username')
    return response