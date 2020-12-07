from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=64)
    cost = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(blank=True, upload_to=None, height_field=None, width_field=None)
    users = models.ManyToManyField(User)
    
    def __str__(self):
        return f"{self.title}, ${self.cost}"

class Watchlisted(models.Model):
    users = models.ManyToManyField(User)
    listings = models.ManyToManyField(Listing)
    trueOrFalse = False

class Bid(models.Model):
    spent = models.DecimalField(max_digits=9, decimal_places=2, unique=True)
    users = models.ManyToManyField(User)
    listings = models.ManyToManyField(Listing)

    
    def __str__(self):
        return f"{self.user}: {self.spent}"

class Comment(models.Model):
    description = models.EmailField(max_length=64)
    likes = models.IntegerField(auto_created=True, default=0)
    users = models.ManyToManyField(User)
    listings = models.ManyToManyField(Listing)
    
    def __str__(self):
        return f"{self.user}: {self.description}"
