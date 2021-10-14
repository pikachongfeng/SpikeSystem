##forms负责处理用户的输入
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.contrib.auth import get_user_model
from . import utils

class LoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(LoginForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs = {'placeholder' : u'用户名', 'class' : 'form-control'}) #form-control为实现一些设计上的定制效果
        self.fields['password'].widget = widgets.PasswordInput(attrs = {'placeholder' : u'密码', 'class' : 'form-control'})

class RegisterForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs = {'placeholder' : u'用户名', 'class' : 'form-control'})
        self.fields['email'].widget = widgets.EmailInput(attrs = {'placeholder' : u'邮箱', 'class' : 'form-control'})
        self.fields['password1'].widget = widgets.PasswordInput(attrs = {'placeholder' : u'输入密码', 'class' : 'form-control'})
        self.fields['password2'].widget = widgets.PasswordInput(attrs = {'placeholder' : u'重复密码', 'class' : 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists(): ##get_user_model()实际获取的是settings.AUTH_USER_MODEL指定的User model
            raise ValidationError(u'该邮箱已注册')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(u'两次密码输入不一致')
        return password2

    ## by using class Meta: you get a nested namespace used just to configure the ModelForm in relation to the model
    ## Fields defined declaratively are left as-is, therefore any customizations made to Meta attributes such as widgets, labels, help_texts, or error_messages are ignored; 
    ## these only apply to fields that are generated automatically.
    class Meta: ## A model form has to have a model to work from, and the Meta object configures this.
        model = get_user_model()
        fields = ('username','email') ## explicitly set fields that should be edited in the form, to avoid that when new fields added to models, users unexpectedyl set them
    
#class EditProfileFrom(forms.ModelForm):
 #   class Meta:
  #      model = UserProfile
   #     fields = ('mobile','address','email','photo') ##fields to edit

class ForgetPasswordForm(forms.Form):
    old_password = forms.CharField(label = u'旧密码',max_length = 16,widget = widgets.PasswordInput(attrs = {'placeholder' : u'旧密码', 'class' : 'form-control'}))
    new_password1 = forms.CharField(label = u'新密码',max_length = 16,widget = widgets.PasswordInput(attrs = {'placeholder' : u'输入新密码', 'class' : 'form-control'}))
    new_password2 = forms.CharField(label = u'重复密码',max_length = 16,widget = widgets.PasswordInput(attrs = {'placeholder' : u'重复新密码', 'class' : 'form-control'}))
    email = forms.EmailField(label = u'邮箱', max_length = 20, widget = widgets.EmailInput(attrs = {'placeholder' : u'邮箱', 'class' : 'form-control'}))
    code = forms.CharField(label = u'验证码',max_length = 4,widget = widgets.TextInput(attrs = {'placeholder' : u'验证码', 'class' : 'form-control'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(u'两次密码输入不一致')
        return password2

    def clean_email(self):
        user_email = self.cleaned_data.get("email")
        if not User.objects.filter(email = user_email).exists():
            raise ValidationError(u'没有找到对应的邮箱')
        return user_email
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        error = utils.verify(email = self.cleaned_data.get('email'),code = code)
        if error:
            raise ValidationError(error)
        return code
    
