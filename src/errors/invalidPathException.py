class InvalidPathException(Exception):
    """An exception that occurs when an path of the level does not lead to a bastion"""

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message
