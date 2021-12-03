from django.db import models
from django.db.models.fields import BooleanField, CharField
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User

class Building(models.Model): 
    Building_ID = models.CharField(max_length = 10,null=True,blank=True)

    class Meta:
        ordering = ['Building_ID']
        db_table = 'tb_buildings'

    def __str__(self):
        return self.Building_ID

class Unit(models.Model):
    building_id = models.ForeignKey(Building,on_delete=models.CASCADE,related_name='build_unit')
    Unit_ID = models.CharField(max_length = 5, verbose_name = u'单元号')
    
    class Meta:
        ordering = ['building_id']
        db_table = 'tb_units'

    def __str__(self):
        return self.building_id.__str__() + ' ' + self.Unit_ID

class Room(models.Model):
    unit_id = models.ForeignKey(Unit,on_delete=models.CASCADE,related_name='unit_room')
    room_id = models.CharField(max_length = 10,verbose_name=u'房间号')
    gender = models.CharField(max_length = 1)
    total_bed = models.IntegerField(verbose_name=u'总床位数')
    avail_bed = models.IntegerField(verbose_name=u'可用床位数')
    unuseable_bed = models.IntegerField(verbose_name=u'坏床数')

    class Meta:
        ordering = ['unit_id']
        db_table = 'tb_rooms'

class Order(models.Model):
    user = OneToOneField(User,on_delete=models.CASCADE,related_name=u'OrderOfUser')
    unit_id = models.ForeignKey(Unit,on_delete=models.CASCADE,related_name='unit_order')    
    gender = models.CharField(max_length = 1,verbose_name=u'性别')
    num_of_stu = models.IntegerField(verbose_name=u'人数')
    success = models.BooleanField(default=False)
    submit_time = models.DateField(auto_now_add=True,verbose_name=u'提交时间')

    class Meta:
        ordering = ['user']
        db_table = 'tb_orders'

class Order_Detail(models.Model):
    order = OneToOneField(Order,on_delete=models.CASCADE,related_name=u'订单号')
    room_id = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='order_room')
    roommate1 = OneToOneField(User,null=True,on_delete=models.CASCADE,related_name=u'同住人1')
    roommate2 = OneToOneField(User,null=True,on_delete=models.CASCADE,related_name=u'同住人2')
    roommate3 = OneToOneField(User,null=True,on_delete=models.CASCADE,related_name=u'同住人3')

    class Meta:
        ordering = ['order']
        db_table = 'tb_orderDetails'

class StuToRoom(models.Model):
    student = OneToOneField(User,on_delete=models.CASCADE,related_name=u'学生名')
    room = OneToOneField(Room,on_delete=models.CASCADE,related_name=u'房间号')
    start_time = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    state = BooleanField(default = False)

    class Meta:
        ordering = ['student']
        db_table = 'tb_stuToRooms'

class CheckOut(models.Model):
    student = OneToOneField(User,on_delete=models.CASCADE,related_name=u'订单提交者')
    room = OneToOneField(Room,on_delete=models.CASCADE,related_name=u'订单房间号')
    time = models.DateField(auto_now_add=True,verbose_name=u'退宿时间')
    operator = CharField(max_length = 10, verbose_name=u'操作人')

    class Meta:
        ordering = ['student']
        db_table = 'tb_checkOuts'
