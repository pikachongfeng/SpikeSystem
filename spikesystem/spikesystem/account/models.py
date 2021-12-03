from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = CASCADE)
    real_name = models.CharField(max_length = 10, verbose_name = u'姓名')
    gender = models.CharField(max_length = 1,verbose_name = u'性别')
    stuID = models.CharField(max_length = 11, verbose_name = u'学号')
    
    class Meta:
        db_table = 'tb_userProfiles'

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)