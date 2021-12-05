from spikesystem.celery import app
from django.db.models import F,Q
from .models import Room,Unit
from django.contrib.auth.models import User
import random
from django.core.cache import cache

@app.task
def create_order(username,unit_id,count):
    user = User.objects.get(username = username)
    select = Unit.objects.get(id = unit_id)
    rooms = Room.objects.filter(Q(unit_id = select) & Q(avail_bed__gte=count))
    room_num = len(rooms)
    random_index = random.randint(0,room_num-1) ##从符合条件的房间里随机选择一个
    selected = rooms[random_index]
    roomID = selected.room_id
    Room.objects.filter(room_id = roomID).update(avail_bed = F('avail_bed') - count) ##选择成功后更新空床数
    cache.set(str(user),1)
    return selected.id
    