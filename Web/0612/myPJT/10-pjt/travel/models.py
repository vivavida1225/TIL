from django.db import models
from django.conf import settings

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('country', 'name')
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.country.name})"

class Travel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='travels')
    countries = models.ManyToManyField(Country, related_name='travels')
    cities = models.ManyToManyField(City, related_name='travels')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date', '-created_at']
        
    def __str__(self):
        return f"{self.user.username}'s travel ({self.start_date} ~ {self.end_date})"
