"""Module containing text functionalities"""
import json

import requests

from .exception import TextResponseException


class TextService:
    """Class for text service"""

    def __init__(self, base_url: str) -> None:
        """Initialize text service"""
        self._base_url = base_url

    def text_completion(self, text: str, **kwargs) -> dict:
        """Run text completion with LLM based on provided parameters"""
        url = f"{self._base_url}/text/text_completion"
        payload = json.dumps({"prompt": text, **kwargs})
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise TextResponseException(response.text)
        return response.json()

    def chat_completion(self, **kwargs) -> dict:
        """Run text completion with LLM based on provided parameters"""
        url = f"{self._base_url}/text/chat_completion"
        payload = json.dumps({**kwargs})
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise TextResponseException(response.text)
        return response.json()
