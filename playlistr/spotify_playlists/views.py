from django.shortcuts import render
from django.http import HttpResponse
from spotify_playlists.services import API
from os import path
from spotify_playlists.models import User

module_dir = path.dirname(__file__)
file_path = path.join(module_dir, "secret.txt")
f = open(file_path, "r")
client_secret = f.readline()
api = API(
    "38c7aa7c8b0a4172aa46a5b7833b8454",
    client_secret,
    "user-read-private user-read-email",
    "http://127.0.0.1:8000/redirect"
)


def index(request):
    context = {
        "spotify_auth_url": api.get_auth_request_url()
    }
    return render(request, "spotify_playlists/index.html", context=context)


def redirect(request):
    user = api.get_login_tokens(request.GET.get('code'))
    profile = api.get_current_user_profile(user['access_token'])
    user['spotify_email'] = profile['email']
    user['id'] = profile['id']
    u = User(**user)
    u.save()
    request.session['id'] = u.id
    return HttpResponse("Hello {}, your email is {}".format("X", "Y"))
