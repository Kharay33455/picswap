from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Images(models.Model):
    name = models.CharField(max_length = 30)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    is_featured = models.BooleanField()
    date_uploaded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
