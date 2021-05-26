from django.urls import path, include
from . import views



urlpatterns = [
    path('road_segment/', views.RoadList.as_view()),
    path('road_segment/<int:id>/', views.RoadDetail.as_view()),
    path('road_speed/', views.RoadSpeedList.as_view()),
    path('road_speed/<int:road_id>/', views.RoadSpeedSegmentList.as_view()),
    path('road_speed/<int:road_id>/<str:time>', views.RoadSpeedSegmentDetail.as_view()),
    path('upload_csv/', views.FileUploadView.as_view()),
]
