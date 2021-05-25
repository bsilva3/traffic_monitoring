from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
#router.register(r'roads', views.RoadViewSet, base_name='roads')
#router.register('road_segment/<int:id>/', views.road_segment)
#router.register('road_segments/', views.road_segments),

urlpatterns = [
    #path('roads', views.RoadViewSet),
    path('road_segment/<int:id>/', views.road_segment),
    path('road_segments/', views.road_segments),
]
