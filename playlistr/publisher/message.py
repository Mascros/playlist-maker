class Message:
    def __init__(self, source, delete):
        if not callable(delete):
            raise TypeError("delete must be a callable")
        if type(source) is not dict:
            raise TypeError("source must be a dict")

        self._source = source
        self._delete = delete
        self._is_deleted = False

    def delete_from_queue(self):
        if self._is_deleted:
            raise AlreadyDeletedError()

        self._delete()
        self._is_deleted = True

    def data(self):
        return self._source

class AlreadyDeletedError(Exception):
    def __init__(self, message="This message has already been deleted"):
        self.message = message
