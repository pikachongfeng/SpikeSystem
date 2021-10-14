from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    #用正则表达式捕捉url，之后调用views.py里的函数Register和Login
    url(r'^register/$',views.Register,name = 'register'),
    url(r'^login/$',views.Login,name = 'login'),
    url(r'^index/$',views.index,name = 'index'),
    url(r'^logout/$',views.logout,name = 'logout'),
    #以下是暂未实现的功能
    #url(r'^forget_password/$',views.ForgetPasswordView.as_view(),name = 'forget_password'),
    #url(r'^validation_code/$',views.ValidationCodeView.as_view(),name = 'validation_code'),
    #url(r'^edit_account/$',views.EditAccountView.as_view(),name = 'edit_accout'),
    #url(r'^logout/$',views.LogoutView.as_view(success_url = '/'),name = 'logout'),
]
