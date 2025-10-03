import traceback

ERROR_CODES = {

 'ChannelNotFound': 1001

}

class _StringMessage:
    def __str__(self):
        return f"{type(self).__name__}: {self.message} (Code: {self.error_code})"


class ChannelNotFound(KeyError, _StringMessage):
    def __init__(self, message="Channel not found in the loaded data", error_code=None):
        super().__init__(message)
        self.message = f"{message}"
        self.error_code = error_code if error_code else ERROR_CODES['ChannelNotFound']