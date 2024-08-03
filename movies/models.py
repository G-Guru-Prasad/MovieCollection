from django.db import models
from django.contrib.auth.models import User
import uuid

# Using auth_user table from django for User records

class Movie(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    genres = models.CharField(max_length=255)

class Collection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    movies = models.ManyToManyField(Movie, related_name='collections')
