from django.db import models


class User(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    spotify_email = models.EmailField()
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    access_token_expiry = models.DateTimeField()


class UserPartyJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True)


class Party(models.Model):
    id = models.AutoField(primary_key=True)
    target_duration_time = models.PositiveIntegerField()
    last_used = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL)
