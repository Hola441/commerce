from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Categories(models.Model):
    categoryTitle = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.categoryTitle}"

class Listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=64)
    cost = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.URLField(blank=True)
    users = models.ManyToManyField(User)
    categoryList = models.ManyToManyField(Categories, related_name="categoryList")
    
    def __str__(self):
        return f"{self.title}, ${self.cost}"

class Watchlisted(models.Model):
    yesOrNo = models.BooleanField()
    users = models.ManyToManyField(User, related_name="watchlisted")
    listings = models.ManyToManyField(Listing, related_name="watchlisted")

class Bid(models.Model):
    spent = models.DecimalField(max_digits=9, decimal_places=2, unique=True)
    users = models.ManyToManyField(User, related_name="bids")
    listings = models.ManyToManyField(Listing, related_name="bids")

    
    def __str__(self):
        return f"{self.users}: ${self.spent}"

class Comment(models.Model):
    description = models.CharField(max_length=64)
    likes = models.IntegerField(auto_created=True, default=0)
    users = models.ManyToManyField(User, related_name="comments")
    listings = models.ManyToManyField(Listing, related_name="comments")
    
    def __str__(self):
        return f"{self.users}: {self.description}"
