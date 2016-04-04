from django.db import models
from datetime import datetime
from django.core.exceptions import FieldError


class User(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    spotify_email = models.EmailField()
    access_token = models.CharField(max_length=163)
    refresh_token = models.CharField(max_length=131)
    token_expiry = models.DateTimeField()

    def token_expired(self):
        if self.access_token == "":
            raise FieldError("User has no access token")
        else:
            if datetime.now() < self.token_expiry:
                return False
            else:
                return True

    def __str__(self):
        return "<User> with id: {}, email {}, tok_exp {}".format(self.id, self.spotify_email, self.token_expiry)


class Party(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    target_no_songs = models.PositiveIntegerField()
    last_used = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    users = models.ManyToManyField(User, related_name='users', related_query_name='user')

    def __str__(self):
        return "<Party> with id: {}, creator {}".format(self.id, self.creator)
