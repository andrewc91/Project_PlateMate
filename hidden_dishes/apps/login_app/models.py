from __future__ import unicode_literals
from django.db import models
import bcrypt, re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r"^[a-zA-Z\s]+$")

# Create your models here.
class ClientManager(models.Manager):
    def register(self, input):
        errors = []

        if len(input['name']) < 3:
            errors.append('Name can not be less than 3 characters')

        if not name_regex.match(input['name']):
            errors.append('Name can contain letters only')

        if not email_regex.match(input['email']):
            errors.append('Not a valid email')

        if len(input['email']) == 0:
            errors.append('Please enter an email')

        if input['password'] != input['confirm']:
            errors.append('Passwords do not match. Try again')

        if len(input['password']) < 8:
            errors.append('Password must be at least 8 characters')

        same = Client.objects.filter(email=input['email'])
        if same:
            errors.append('Email is already in use')

        if len(errors) == 0:
            pwHash = bcrypt.hashpw(input['password'].encode(), bcrypt.gensalt().encode())
            user = Client.objects.create(name=input['name'], email=input['email'], password=pwHash)
            return (True, user)

        else:
            return (False, errors)

    def login(self, input):
        errors = []
        user = Client.objects.filter(email=input['email'])
        if user.exists():
            InputPw = input['password'].encode()
            HashPw = user[0].password.encode()

            if bcrypt.checkpw(InputPw, HashPw):
                return (True, user[0])
            else:
                errors.append(("Email or password match doesn't exist!"))
        else:
            errors.append(("Email or password match doesn't exist!"))
        return (False, errors)

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ClientManager()
