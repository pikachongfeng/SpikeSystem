from rest_framework import serializers
from account.models import UserProfile
from .models import Room,Order,Order_Detail
from .models import Room,Order,Order_Detail
from django.contrib.auth.models import User
from django.db.models import F
import random
from django.db.models import Q
from django.core.cache import cache
import time

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'unit_id',
            'room_id',
            'gender',
            'avail_bed',
        ]

class UsernameSerializer(serializers.ModelSerializer):
    room_id = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = User
        fields = [
            'username',
            'room_id',
        ]
        
    def get_room_id(self,obj):
        selected_order = obj.OrderOfUser
        order_detail = Order_Detail.objects.get(order = selected_order)
        return RoomIDSerializer(order_detail.room_id).data
    
class RoomIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_id']

class OrderPostSerializer(serializers.ModelSerializer):
    roommate1 = serializers.CharField(allow_blank = True,write_only = True) ##添加没有的字段，默认只读
    roommate2 = serializers.CharField(allow_blank = True,write_only = True)
    roommate3 = serializers.CharField(allow_blank = True,write_only = True)
    class Meta:
        model = Order
        fields = [
            'user',
            'unit_id',
            'roommate1',
            'roommate2',
            'roommate3',
        ]
        read_only_fields = ['user']

    def create(self,validated_data):
        user = self.context.get('request').user
        mate1 = validated_data['roommate1']
        mate2 = validated_data['roommate2']
        mate3 = validated_data['roommate3']
        select = validated_data['unit_id']
        count = 1
        if mate1 != '':
            if not User.objects.filter(username = mate1):
                raise serializers.ValidationError("同住人1不存在")
            count+=1
        if mate2 != '':
            if not User.objects.filter(username = mate2):
                raise serializers.ValidationError("同住人2不存在")
            count+=1
        if mate3 != '':
            if not User.objects.filter(username = mate3):
                raise serializers.ValidationError("同住人3不存在")
            count+=1
        if Order.objects.filter(user = user): ##判断用户是否已经提交过订单
            raise serializers.ValidationError("已经提交过订单")
        userprofile = UserProfile.objects.get(user = user)
        if not userprofile: ##判断用户是否填写自己的个人信息
            raise serializers.ValidationError("未填写个人信息")
        gender = userprofile.gender
        if cache.get('gender_of_') != gender:
            raise serializers.ValidationError("该单元不符合你的性别")
        if not Room.objects.filter(Q(unit_id = select) & Q(avail_bed__gte=count)).exists(): ##判断该单元是否有空床
            raise serializers.ValidationError("该单元空床不足")
        rooms = Room.objects.filter(Q(unit_id = select) & Q(avail_bed__gte=count))
        room_num = len(rooms)
        random_index = random.randint(0,room_num-1) ##从符合条件的房间里随机选择一个
        selected = rooms[random_index]
        roomID = selected.room_id
        Room.objects.filter(room_id = roomID).update(avail_bed = F('avail_bed') - count) ##选择成功后更新空床数
        create_order = Order.objects.create(user = user,unit_id = selected.unit_id, num_of_stu = count, success = 1, submit_time = time.time(), gender = gender) ##选择有效就创建订单
        order = Order.objects.get(user = user)
        if count == 1:
            Order_Detail.objects.create(order = order,room_id = selected)
        if count == 2:
            Order_Detail.objects.create(order = order,room_id = selected,roommate1 = mate1)
        if count == 3:
            Order_Detail.objects.create(order = order,room_id = selected,roommate1 = mate1, roommate2 = mate2)
        if count == 4:
            Order_Detail.objects.create(order = order,room_id = selected,roommate1 = mate1, roommate2 = mate2, roommate3 = mate3)
        return create_order