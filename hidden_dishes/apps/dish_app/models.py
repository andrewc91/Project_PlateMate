from __future__ import unicode_literals
from ..login_app.models import Client
from django.db import models

# Create your models here.

class RestaurantManager(models.Manager):
    def restaurant_validator(self, input):
        errors = []

        if len(input['restaurant']) == 0:
            errors.append("Please enter in a restaurant")

        if len(input['restaurant']) < 3:
            errors.append("Restaurant name must be at least 3 characters")

        if len(errors) == 0:
            return (True, ["Success"])

        else:
            return (False, errors)

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

        # if len(request.FILES['picture']) == 0:
        #     errors.append("Please upload a picture of the dish")

        if len(errors) == 0:
            return (True, ["Plate Added"])
        else:
            return (False, errors)

    def add_like(self, user_id, plate_id):
        plate = self.get(id=plate_id)
        user = Client.objects.get(id=user_id)
        plate.likes.add(user)
        plate.save()
        return True

class Plate(models.Model):
    name = models.CharField(max_length=100)
    review = models.TextField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(Client)
    restaurant = models.ForeignKey(Restaurant)
    likes = models.ManyToManyField(Client, related_name="plates")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PlateManager()

class CommentManager(models.Manager):
    def comment_validator(self, input, user, id):
        errors = []

        if len(input['comment']) == 0:
            errors.append("Please enter in a comment")

        if len(input['comment']) < 2:
            errors.append("Comment must be at least 2 characters")

        if len(errors) == 0:
            user = Client.objects.get(id=user)
            plate = Plate.objects.get(id=id)
            comment = Comment.objects.create(text=input['comment'], user=user, plate=plate)
            return (True, comment, id)
        else:
            return (False, errors)

class Comment(models.Model):
    text = models.TextField(max_length=255)
    user = models.ForeignKey(Client)
    plate = models.ForeignKey(Plate)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
