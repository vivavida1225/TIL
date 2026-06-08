from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('create/', views.create_travel, name='create_travel'),
    path('delete/<int:travel_id>/', views.delete_travel, name='delete_travel'),
]
