from django.db import models
from datetime import datetime


class User(models.Model):
    _id = models.CharField(max_length=64, primary_key=True)
    _spotify_email = models.EmailField()
    _access_token = models.CharField(max_length=200)
    _refresh_token = models.CharField(max_length=200)
    _token_expiry = models.DateTimeField()

    def token_expired(self):
        if datetime.now() < self.access_token_expiry:
            return False
        else:
            return True


class Party(models.Model):
    _id = models.AutoField(primary_key=True)
    _target_duration_time = models.PositiveIntegerField()
    _last_used = models.DateTimeField()
    _creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class UserPartyJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True)
