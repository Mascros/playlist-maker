from django.db import models
from datetime import datetime


class User(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    spotify_email = models.EmailField()
    access_token = models.CharField(max_length=163)
    refresh_token = models.CharField(max_length=131)
    token_expiry = models.DateTimeField()

    def token_expired(self):
        if datetime.now() < self.access_token_expiry:
            return False
        else:
            return True

    def __str__(self):
        return "<User> with id: {}, email {}, tok_exp {}".format(self.id, self.spotify_email, self.token_expiry)


class Party(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    target_duration_time = models.PositiveIntegerField()
    last_used = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    party_start_date = models.DateField()

    def __str__(self):
        return "<Party> with id: {}, creator {}".format(self.id, self.creator)


class UserPartyJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "<UserPartyJoin> between user id: {} and party id:{}".format(self.user.id, self.party.id)
