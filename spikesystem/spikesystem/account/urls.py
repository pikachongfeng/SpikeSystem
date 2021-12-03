from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()


from django.urls import path

router.register(r'user', views.UserViewSet)
router.register(r'edit', views.ProfileViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
