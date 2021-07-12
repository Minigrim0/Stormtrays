class InvalidPositionException(Exception):
    """An exception that occurs when the position of an event is not correct"""

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message
