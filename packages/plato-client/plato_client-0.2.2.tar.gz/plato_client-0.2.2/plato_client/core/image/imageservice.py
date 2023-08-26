"""Module containing image functionalities"""
import json

import requests
from .exception import ImageResponseException


class ImageService:
    """Class for image service"""

    def __init__(self, base_url: str) -> None:
        """Initialize image service"""
        self._base_url = base_url

    def create(self, **kwargs) -> dict:
        """Run text completion with LLM based on provided parameters"""
        url = f"{self._base_url}/image/create"
        payload = json.dumps({**kwargs})
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise ImageResponseException(response.text)
        return response.json()
