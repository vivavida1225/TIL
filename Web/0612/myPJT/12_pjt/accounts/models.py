from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    kakao_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    profile_image_url = models.URLField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nickname = models.CharField(max_length=50, unique=True, null=True, blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return f"{self.username} (Kakao: {self.kakao_id})" if self.kakao_id else self.username

class PreferenceChoice(models.Model):
    CATEGORY_CHOICES = (
        ('STYLE', 'Sightseeing Style'),
        ('TASTE', 'Taste Preference'),
    )
    key = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"[{self.category}] {self.name}"

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    hygiene_sensitivity = models.IntegerField(null=True, blank=True)
    preparedness = models.IntegerField(null=True, blank=True)
    choices = models.ManyToManyField(PreferenceChoice, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"

