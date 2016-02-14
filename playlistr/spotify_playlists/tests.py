from datetime import datetime
from django.test import TestCase
from django.core.exceptions import FieldError

from .models import User


class UserMethodTests(TestCase):
    def test_token_expired_with_expired(self):
        """
        token_expired() should return true when the token expiry date is in the past
        """
        user = User(token_expiry=datetime.min, access_token="blah")
        self.assertTrue(user.token_expired())

    def test_token_expired_with_future(self):
        """
        token_expired() should return false when the token expiry date is in the future
        """
        user = User(token_expiry=datetime.max, access_token="blah")
        self.assertFalse(user.token_expired())

    def test_token_expired_with_no_access(self):
        """
        token_expired() should throw a FieldError when the user has no access token
        """
        user = User(token_expiry=datetime.max)
        self.assertRaises(FieldError, user.token_expired)
