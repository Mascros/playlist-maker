from unittest import TestCase
from publisher.messagereceiver import MessageReceiver
from publisher.message import Message

json_message = {
                    'creator': {},
                    'users': [],
                    'name': 'a_party',
                    'target_no_songs': 12
                }
class MockService:
    def __init__(self, no_of_messages):
        self._messages = [json_message] * no_of_messages

    def receive_messages(self):
        return self._messages


class TestMessageReceiver(TestCase):
    def test_get_messages_no_messages(self):
        """should return an empty list if there are no messages"""
        receiver = MessageReceiver(MockService(0), Message)
        messages = receiver.get_messages()
        self.assertEqual(messages, [])

    def test_get_messages(self):
        """should return the list of messages"""
        count = 3
        receiver = MessageReceiver(MockService(count), Message)
        messages = receiver.get_messages()
        self.assertEqual(messages, [json_message] * count)