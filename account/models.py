from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,User
from django.db.models.fields.related import OneToOneField

class User(AbstractUser): ##AbstractUser类中包含username, password, email,抽象基类不会创建数据表
    ##AbstractUser中的username,password,email都已经对输入格式有了限制
    #mobile = models.CharField(max_length = 11, unique=True, verbose_name=u'手机号') #max_length参数限制长度

    class Meta: ##meta创建元数据，即“所有不是字段的东西”
        ordering = ['id']
        verbose_name = u'用户'
        verbose_name_plural = verbose_name
        db_table = 'tb_users'

#class UserProfile(models.Model):
    #user = models.OneToOneField(User,on_delete=models.CASCADE) ##on_delete=models.CASCADE表示当User被删除时，user也会被删除
    #data_of_birth = models.DateField(blank=True,null=True,verbose_name='生日')
    #photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True,verbose_name=u'照片') ##django在upload_to上内置了strftime()函数
    #score = models.IntegerField(default=0,verbose_name=u'积分')
    #gender = models.CharField(max_length = 1,verbose_name = u'性别')
    #address = models.CharField(max_length = 50, verbose_name = u'地址')
    
    #def __str__(self):
        #return 'Profile for user {}'.format(self.user.username)
    

