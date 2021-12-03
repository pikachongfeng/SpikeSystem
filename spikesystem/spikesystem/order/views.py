import logging
from re import search

from django.contrib.auth.models import User
from .models import Room,Order
from .serializers import RoomListSerializer
from rest_framework.response import Response
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