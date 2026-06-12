from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('board/', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('detail/<int:post_id>/like/', views.post_like, name='post_like'),
    path('detail/<int:post_id>/scrap/', views.post_scrap, name='post_scrap'),
    path('detail/<int:post_id>/comment/', views.comment_create, name='comment_create'),
    path('detail/<int:post_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]
