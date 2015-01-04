import binascii
import os
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


class Token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='authtoken')
    token = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super(Token, self).save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __unicode__(self):
        return self.token
