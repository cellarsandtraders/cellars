from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.db.models.signals import post_save
# from django.contrib.sites.models import Site
# from actstream import action


class DateTimeAware(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(AbstractUser, DateTimeAware):
    #Add other user attributes here
    cellar = models.ManyToManyField("CellarItem", related_name='cellar')
    wants = models.ManyToManyField("CellarItem", related_name='wishlist')

    API_FIELDS = [
        "username", "wants", "first_name", "last_name", "created",
        "is_active", "modified", "is_superuser", "is_staff", "last_login",
        "groups", "user_permissions", "email", "cellar", "date_joined",
    ]


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
        return self.name


# Post save stuff

# def user_registered_action(sender, instance, created, **kwargs):
#     if created:
#         current_site = Site.objects.get_current()
#         action.send(instance, verb="joined", target=current_site)

#post_save.connect(user_registered_action, sender=User)
