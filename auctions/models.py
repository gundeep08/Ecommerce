from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    owner= models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    image = models.ImageField(upload_to='images/', blank=True)
    isListingAvailable = models.BooleanField(default=True)

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True,  null=True, related_name="comment")
    comment = models.CharField(max_length=120)


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True,  null=True, related_name="bid")
    bidPrice = models.IntegerField()
    highestBidder= models.CharField(max_length=64, blank=True)


class Watchlist(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watchlist")

