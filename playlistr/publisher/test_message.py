from unittest import TestCase
from unittest.mock import Mock
from publisher.message import Message, AlreadyDeletedError

class TestMessage(TestCase):
    @staticmethod
    def _delete():
        pass

    def test_init_wrong_delete_type(self):
        """should raise a TypeError if delete is not callable"""
        with self.assertRaises(TypeError):
            message = Message({
                    'creator': {},
                    'users': [],
                    'name': 'a_party',
                    'target_no_songs': 12
                }, "NOT A CALLABLE")

    def test_init_wrong_source_type(self):
        """should raise a TypeError if source is not a dict"""
        with self.assertRaises(TypeError):
            message = Message("", self._delete)

    def test_delete_from_queue_already_deleted(self):
        """raise an AlreadyDeletedError if already delted"""
        message = Message({
                    'creator': {},
                    'users': [],
                    'name': 'a_party',
                    'target_no_songs': 12
                }, self._delete)
        message.delete_from_queue()
        with self.assertRaises(AlreadyDeletedError):
            message.delete_from_queue()

    def test_delete_from_queue(self):
        """should call the delete argument"""
        mock_delete = Mock(return_value=None)
        message = Message({
                    'creator': {},
                    'users': [],
                    'name': 'a_party',
                    'target_no_songs': 12
                }, mock_delete)
        message.delete_from_queue()
        mock_delete.assert_called_once_with()

    def test_data(self):
        """should return the original message data as a dict"""
        original = {
                    'creator': {},
                    'users': [],
                    'name': 'a_party',
                    'target_no_songs': 12
                }
        message = Message(original, self._delete)
        self.assertEqual(original, message.data())


    def test_data_after_delete(self):
        """should return the original message data as a dict

        deleting should only delete from the queue,
        the data should exist until not referenced
        """
        original = {
                    'creator': {},
                    'users': [],
                    'name': 'a_party',
                    'target_no_songs': 12
                }
        message = Message(original, self._delete)
        message.delete_from_queue()
        self.assertEqual(original, message.data())
