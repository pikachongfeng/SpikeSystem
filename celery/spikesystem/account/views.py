import logging


from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .serializers import UserRegisterSerializer,UserProfileSerializer
from .permissions import IsSelfOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response


logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]

        return super().get_permissions()
    
    @action(detail=True, methods=['get'])
    def info(self, request, username=None):
        queryset = User.objects.get(username=username)
        serializer = UserRegisterSerializer(queryset, many=False)
        return Response(serializer.data)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    