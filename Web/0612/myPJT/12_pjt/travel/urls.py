from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('create/', views.create_travel, name='create_travel'),
    path('delete/<int:travel_id>/', views.delete_travel, name='delete_travel'),
    path('<int:travel_id>/videos/', views.travel_videos, name='travel_videos'),
    path('videos/detail/<str:video_id>/', views.video_detail, name='video_detail'),
    path('videos/saved/', views.saved_videos, name='saved_videos'),
    path('videos/channels/', views.saved_channels, name='saved_channels'),
]
