from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from actstream import action


class DateTimeAware(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(AbstractUser, DateTimeAware):
    #Add other user attributes here
    cellar = models.ManyToManyField("CellarItem", related_name='cellar')
    wishlist = models.ManyToManyField("CellarItem", related_name='wishlist')

    def to_json(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created": self.created.isoformat(),
            "modified": self.modified.isoformat(),
            "date_joined": self.date_joined.isoformat(),
            "last_login": self.last_login.isoformat(),
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "is_staff": self.is_staff,
            "cellar": [x.id for x in self.cellar.all()],
            "wishlist": [x.id for x in self.wishlist.all()],
        }


class CellarItem(DateTimeAware):
    beer_id = models.CharField(max_length=32, null=True)
    beer_name = models.CharField(max_length=200)
    brewery_id = models.CharField(max_length=32, null=True)
    brewery_name = models.CharField(max_length=500)
    style = models.CharField(max_length=200, blank=True)
    abv = models.FloatField(blank=True, null=True)
    year = models.CharField(max_length=4, blank=True)
    quantity = models.IntegerField(default=1)
    willing_to_trade = models.BooleanField(default=True)
    label = models.URLField(blank=True)

    def __unicode__(self):
        return self.beer_name

    def to_json(self):
        return {
            "id": self.id,
            "beer_id": self.beer_id,
            "beer_name": self.beer_name,
            "brewery_id": self.brewery_id,
            "brewery_name": self.brewery_name,
            "style": self.style,
            "abv": self.abv,
            "year": self.year,
            "quantity": self.quantity,
            "willing_to_trade": self.willing_to_trade,
            "label": self.willing_to_trade
        }


# Post save stuff

def user_registered_action(sender, instance, created, **kwargs):
    if created:
        action.send(instance, verb="joined")

post_save.connect(user_registered_action, sender=UserProfile)
