import logging

from django.core.cache import cache
from django.http.response import HttpResponse
from .models import Unit
from .models import Room,Order
from .serializers import RoomListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .serializers import UsernameSerializer,OrderPostSerializer

logger = logging.getLogger(__name__)

@api_view(['GET',])
def room_list(request):
    rooms = Room.objects.all()
    serializer = RoomListSerializer(rooms, many=True)
    return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderPostSerializer

@api_view(['GET',])
def order_result(request):
    user = request.user
    Userserializer = UsernameSerializer(user)
    return Response(Userserializer.data)

def redis_insert(request):
    Units = Unit.objects.all()
    unit1 = Units[0]
    unit2 = Units[1]
    unit3 = Units[2]
    unit4 = Units[3]
    cache.set('gender_of_' + str(unit1),'男')
    cache.set('gender_of_' + str(unit2),'女')
    cache.set('gender_of_' + str(unit3),'男')
    cache.set('gender_of_' + str(unit4),'女')
    cache.set('zoom_of_' + str(unit1),8)
    cache.set('zoom_of_' + str(unit2),8)
    cache.set('zoom_of_' + str(unit3),8)
    cache.set('zoom_of_' + str(unit4),8)
    return HttpResponse('done!')