from . import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'select',views.OrderViewSet,basename='select_dorm')
urlpatterns = [
    #用正则表达式捕捉url，之后调用views.py里的函数Register和Login
    path('list/',views.room_list,name = 'list'),
    path('result/',views.order_result,name = 'results'),
    path('insert/',views.redis_insert,name = 'redis_insert'),
    path('', include(router.urls)),
]
