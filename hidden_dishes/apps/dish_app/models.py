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
    def plate_validator(self, input):
        errors = []

        if len(input['plate']) == 0:
            errors.append("Please enter in a plate")

        if len(input['plate']) < 3:
            errors.append("Dish name must be at least 3 characters")

        if len(input['review']) == 0:
            errors.append("Please enter in a review")

        # if len(input['file']) == 0:
        #     errors.append("Please upload a picture of the dish")

        if len(errors) == 0:
            Plate.objects.create(name=input['plate'], review=input['review'])
            return (True, ["Plate Added"])
        else:
            return (False, errors)

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
