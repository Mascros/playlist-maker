from datetime import datetime
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.core.exceptions import FieldError
from django.core.urlresolvers import reverse
from unittest.mock import MagicMock

from .models import User
from .services import API

setup_test_environment()
client = Client()


class UserMethodTests(TestCase):
    def setUp(self):
        self.user = User(access_token="blah")

    def test_token_expired_with_expired(self):
        """
        token_expired() should return true when the token expiry date is in the past
        """
        self.user.token_expiry = datetime.min
        self.assertTrue(self.user.token_expired())

    def test_token_expired_with_future(self):
        """
        token_expired() should return false when the token expiry date is in the future
        """
        self.user.token_expiry = datetime.max
        self.assertFalse(self.user.token_expired())

    def test_token_expired_with_no_access(self):
        """
        token_expired() should throw a FieldError when the user has no access token
        """
        user = User(token_expiry=datetime.max)
        self.assertRaises(FieldError, user.token_expired)


class IndexViewTests(TestCase):
    def setUp(self):
        self.res = client.get(reverse('spotify_playlists:index'))

    def test_status_code(self):
        """
        the index view should always return a 200 OK HTTP response
        """
        self.assertEqual(self.res.status_code, 200)

    def test_auth_url(self):
        """
        the index view should always contain an auth url for spotify login
        """
        self.assertIn(b'https://accounts.spotify.com/authorize?', self.res.content)
        self.assertIn(b'response_type=code', self.res.content)

    def tearDown(self):
        self.res.close()


class RedirectViewLoggedInTests(TestCase):
    def setUp(self):
        # Prevent save() from crashing because we don't have the side effects from the methods we stub
        User.save = MagicMock()

        user = {
            'access_token': "token"
        }
        API.get_login_tokens = MagicMock(return_value=user)

        profile = {
            'email': 'test@example.com',
            'id': 'test_user_id'
        }
        API.get_current_user_profile = MagicMock(return_value=profile)
        self.res = client.get(reverse('spotify_playlists:redirect') + "?code=123xyz")

    def test_status_code(self):
        """
        the redirect view should return a 200 OK when the user is Logged in
        """
        self.assertEqual(self.res.status_code, 200)

    def test_user_session(self):
        """
        the redirect view should create a session for the user with their id stored
        """
        self.assertEqual(client.session['id'], 'test_user_id')

    def test_user_saved(self):
        """
        the redirect view should save the user to the database
        """
        # The comment below stops PyCharm from complaining because it doesnt know setUp is always called first
        # noinspection PyUnresolvedReferences
        User.save.assert_called_with()

    def tearDown(self):
        self.res.close()


class RedirectViewFailedLoginTests(TestCase):
    def setUp(self):
        self.res = client.get(reverse('spotify_playlists:redirect'))

    def test_assert_redirect_to_index(self):
        """
        the redirect view should redirect the user to the index view if they are not logged in
        """
        self.assertEqual(self.res.status_code, 302)
        self.assertEqual(self.res.url, '/')


class StartPartyViewHappyTests(TestCase):
    """
    User is authenticated (has a session with an id)
    """
    def setUp(self):
        self.res = client.get(reverse('spotify_playlists:testing_session'))
        self.res = client.post(reverse('spotify_playlists:start'), data={'party_name': 'test_party_name'})

    def test_status_code(self):
        """
        the status code should be 200 if the user is logged in
        """
        self.assertEqual(self.res.status_code, 200)

    def test_party_name_in_body(self):
        """
        the name user chose for the party should be displayed on the page
        """
        self.assertIn(b'test_party_name', self.res.content)

    def test_start_party_in_content(self):
        """
        'Start Party' should appear somewhere in the response content
        """
        self.assertIn(b'Start Party', self.res.content)

    def tearDown(self):
        self.res.close()


class StartPartyViewSadTests(TestCase):
    """
    User is not authenticated (has no id or session)
    """
    def setUp(self):
        self.res = client.get(reverse('spotify_playlists:start'), data={'party_name': 'test_party_name'}, follow=True)

    def test_redirect_to_index(self):
        self.assertIn(b"Log in with Spotify", self.res.content)
        self.assertIn(b"Playlist Maker - Home", self.res.content)
