from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import redirect as django_redirect
from django.http import HttpResponse
from spotify_playlists.services import API
from playlistr.settings import DEBUG
from os import path
from spotify_playlists.models import User
from django.utils.crypto import get_random_string
import logging

module_dir = path.dirname(__file__)
file_path = path.join(module_dir, "secret.txt")
f = open(file_path, "r")
client_secret = f.readline()
f.close()
api = API(
    "38c7aa7c8b0a4172aa46a5b7833b8454",
    client_secret,
    "user-read-private user-read-email",
    "http://127.0.0.1:8000/redirect"
)

log = logging.getLogger(__name__)


def testing_session(request):
    # Create a session for use in unittests so the test client looks authenticated
    if not DEBUG:
        raise Exception("This view should always be disabled when in production.")
    else:
        log.info("Creating a session for use in testing. id=test_user_id")
        request.session['id'] = 'test_user_id'
        return HttpResponse("Session is created")


def index(request):
    context = {
        "spotify_auth_url": api.get_auth_request_url()
    }
    return render(request, "spotify_playlists/index.html", context=context)


def redirect(request):
    code = request.GET.get('code')
    if code is None:
        return django_redirect(reverse('spotify_playlists:index'))
    user = api.get_login_tokens(code)
    profile = api.get_current_user_profile(user['access_token'])
    user['spotify_email'] = profile['email']
    user['id'] = profile['id']
    u = User(**user)
    u.save()
    request.session['id'] = u.id
    return render(request, 'spotify_playlists/logged_in.html')


def join(request):
    return HttpResponse("Not implemented yet")


def start(request):
    try:
        user_id = request.session['id']
        party_name = request.POST.get('party_name')

    except KeyError:
        log.info("start view: User with no id in session, or did not choose a party name. redirected to index")
        return django_redirect('index')

    else:
        party_id = get_random_string(length=8)
        log.info("User_id '{}' starting party with name '{}' and party_id '{}' ".format(user_id, party_name, party_id))
        context = {
            "party_name": party_name,
            "party_id": party_id
        }
        return render(request, 'spotify_playlists/start_party.html', context=context)


def save_party(request):
    return HttpResponse("Not implemented yet")
