from unittest import TestCase
from publisher.messagereceiver import MessageReceiver
from publisher.message import Message


class MockBotoMessage:
    body = {
        'creator': {},
        'users': [],
        'name': 'a_party',
        'target_no_songs': 12
    }
    def delete(self):
        pass

class MockService:
    def __init__(self, no_of_messages):
        self._messages = [MockBotoMessage] * no_of_messages

    def receive_messages(self):
        return self._messages


class TestMessageReceiver(TestCase):
    def test_get_messages_no_messages(self):
        """should return an empty list if there are no messages"""
        receiver = MessageReceiver(MockService(0), Message)
        messages = receiver.get_messages()
        self.assertEqual(messages, [])

    def test_get_messages(self):
        """should return a list of Message objects

        messages given should have been instantiated as the given Message type
        """
        count = 3
        receiver = MessageReceiver(MockService(count), Message)
        messages = receiver.get_messages()
        self.assertEqual(len(messages), count)
        self.assertIsInstance(messages[0], Message)