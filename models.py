from django.db import models
import re
import bcrypt
# from datetime import datetime


# Create your models here.

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        # checks the email 
        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters"
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['first_name'] = "Your name must be at least 3 characters"
        if not email_regex.match(postData['email']):
            errors['email'] = 'Email must be valid'
        email_check = self.filter(email=postData['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if postData['password'] != postData['confirm']:
            errors['password'] = 'Password and Confirm PW do not match'
        return errors
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())



class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    objects = UserManager()


class WishManager(models.Manager):
    def wish_validate(self, postData):
        errors = {}
        if len(postData['new_wish']) < 3:
            errors['new_wish'] = 'Wish field should be at least 3 characters'
        if len(postData['description']) < 3:
            errors['description'] = 'Description should be at least 3 characters'
        return errors

class Wish(models.Model):
    wish_item= models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_added = models.DateTimeField()
    poster = models.ForeignKey(User, related_name='wisher', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()

