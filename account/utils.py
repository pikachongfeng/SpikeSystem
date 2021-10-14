import typing
from datetime import timedelta
from django.core.cache import cache ##引用默认缓存
import django.dispatch #内置信号集,使用户代码能够获得 Django 自身某些操作的通知

_code_ttl = timedelta(minutes=1) ##timedelta表示两个时间之间的差值

send_email_signal = django.dispatch.Signal( ##所有的信号都是 django.dispatch.Signal 的实例。
    providing_args=['emailto', 'title', 'content'])

def send_email(emailto, title, content):
    send_email_signal.send(
        send_email.__class__, ##sender参数
        emailto=emailto,
        title=title,
        content=content)

def send_verify_email(to_mail:str,code:str,subject : str = u'邮箱验证码'):
    html_content = f"您正在重设密码，验证码为：{code}, 1分钟内有效，请妥善保管"
    send_email([to_mail], subject, html_content)

def verify(email:str,code:str) -> typing.Optional['str']: ##需要str或None
    cache_code = get_code(email)
    if cache_code != code:
        raise ValueError('验证码错误')

def set_code(email:str,code:str):
    cache.set(email,code,_code_ttl.seconds) ##cache.set(key, value, timeout=DEFAULT_TIMEOUT, version=None)¶

def get_code(email:str) -> typing.Optional['str']: 
    return cache.get(email)

