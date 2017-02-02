from __future__ import unicode_literals
from ..login_app.models import Client
from django.db import models

# Create your models here.

class RestaurantManager(models.Manager):
    pass

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RestaurantManager()

class PlateManager(models.Manager):
    pass

class Plate(models.Model):
    name = models.CharField(max_length=100)
    review = models.TextField(max_length=255)
    image = models.ImageField()
    client = models.ForeignKey(Client)
    restaurant = models.ForeignKey(Restaurant)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PlateManager()

class CommentManager(models.Manager):
    pass

class Comment(models.Model):
    text = models.TextField(max_length=255)
    client = models.ForeignKey(Client)
    plate = models.ForeignKey(Plate)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()

class Like(models.Model):
    client = models.ForeignKey(Client)
    plate = models.ForeignKey(Plate)
    liked = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
