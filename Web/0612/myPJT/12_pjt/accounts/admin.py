from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'kakao_id', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Kakao Info', {'fields': ('kakao_id', 'profile_image_url')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Kakao Info', {'fields': ('kakao_id', 'profile_image_url')}),
    )

admin.site.register(User, CustomUserAdmin)
