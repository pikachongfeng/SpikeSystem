import os
from celery import Celery
from django.conf import settings

# 导入django的环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spikesystem.settings')

app = Celery('spikesystem') #实例化一个Celery对象

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() #让Celery自动发现所有的异步任务。Celery会在每个INSTALLED_APPS中列出的应用中寻找task.py文件，在里边寻找定义好的异步任务然后执行。