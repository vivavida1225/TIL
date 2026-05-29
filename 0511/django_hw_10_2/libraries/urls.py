from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:book_pk>/detail/', views.book_detail, name='book_detail'),
    path('<int:book_pk>/', views.book_detail, name='book_detail'),
]
