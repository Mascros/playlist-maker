class MessageReceiver:
    def __init__(self, service, Message):
        self._Message = Message
        self._service = service

    def get_messages(self):
        received = self._service.receive_messages()
        return [self._Message(message.body, message.delete) for message in received]
