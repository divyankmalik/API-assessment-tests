class HttpError(Exception):
    """An error that should be returned to the client with a specific HTTP status."""

    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message
