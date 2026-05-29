from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout, name='logout'),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('additional-info/', views.additional_info, name='additional_info'),
    path('preference/step/<int:step_num>/', views.preference_step, name='preference_step'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('profile/<int:user_id>/follow/', views.follow_user, name='follow_user'),
]
