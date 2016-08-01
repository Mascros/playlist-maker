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

    def get_for_publishing(self):
        data = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'token_expiry': self.token_expiry
        }
        return data

    def __str__(self):
        return "<User> with id: {}, email {}, tok_exp {}".format(self.id, self.spotify_email, self.token_expiry)


class Party(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    target_no_songs = models.PositiveIntegerField()
    last_used = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    users = models.ManyToManyField(User, related_name='users', related_query_name='user')
    admins = models.ManyToManyField(User, related_name='admins', related_query_name='admin')

    def get_for_context(self, request):
        return {
            'name': self.name,
            'creator': self.creator.id,
            'id': self.id,
            'share_url': "http://" + request.get_host() + "/join/" + self.id,
            'users': self.users.all()
        }

    def get_for_publishing(self):
        """
        get a description of the playlist in a format for sending to be published
        :return: dictionary object
        """
        # Additional fields for the creator so that they can be emailed when playlist is ready
        creator = self.creator.get_for_publishing()
        creator['id'] = self.creator.id
        creator['spotify_email'] = self.creator.spotify_email

        data = {
            # Include name so that in the email the ready playlist can be named
            'name': self.name,
            'target_no_songs': self.target_no_songs,
            'creator': creator,
            'users': [user.get_for_publishing() for user in self.users]
        }
        return data

    def __str__(self):
        return "<Party> with id: {}, creator {} and users {}".format(self.id, self.creator, self.users)
