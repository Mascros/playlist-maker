from django.db import models
from datetime import datetime


class User(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    spotify_email = models.EmailField()
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    token_expiry = models.DateTimeField()

    def token_expired(self):
        if datetime.now() < self.access_token_expiry:
            return False
        else:
            return True


class UserPartyJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True)


class Party(models.Model):
    id = models.AutoField(primary_key=True)
    target_duration_time = models.PositiveIntegerField()
    last_used = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL)
