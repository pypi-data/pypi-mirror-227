"""Module implementing image related exceptions"""


class ImageResponseException(Exception):
    """Raised when exception occurs with Image response"""

    def __init__(self, message):
        self.message = message
