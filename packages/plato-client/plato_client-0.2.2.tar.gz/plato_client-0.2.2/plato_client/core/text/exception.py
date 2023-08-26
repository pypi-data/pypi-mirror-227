"""Module implementing text related exceptions"""


class TextResponseException(Exception):
    """Raised when exception occurs LLM response"""

    def __init__(self, message):
        self.message = message
