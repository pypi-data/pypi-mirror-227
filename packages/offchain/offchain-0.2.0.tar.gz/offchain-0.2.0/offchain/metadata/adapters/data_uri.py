import base64
from urllib.request import urlopen

import httpx
from requests import PreparedRequest, Response

from offchain.metadata.adapters.base_adapter import BaseAdapter
from offchain.metadata.registries.adapter_registry import AdapterRegistry


def decode_data_url(data_url):
    data_parts = data_url.split(",")
    data = data_parts[1]

    if ";base64" in data_parts[0]:
        decoded_data = base64.b64decode(data)
        decoded_text = decoded_data.decode("utf-8")
        return decoded_text

    return None


@AdapterRegistry.register
class DataURIAdapter(BaseAdapter):
    """Provides an interface for Requests sessions to handle data uris."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def gen_send(self, url: str, *args, **kwargs) -> httpx.Response:
        """Handle async data uri request.

        Args:
            url (str): url

        Returns:
            httpx.Response: encoded data uri response.
        """
        response = httpx.Response(
            status_code=200,
            text=decode_data_url(url),
            request=httpx.Request(method="GET", url=url),
        )
        return response

    def send(self, request: PreparedRequest, *args, **kwargs):
        """Handle data uri request.

        Args:
            request (PreparedRequest): incoming request

        Returns:
            Response: encoded data uri response.
        """
        newResponse = Response()
        newResponse.request = request
        newResponse.url = request.url
        newResponse.connection = self
        try:
            response = urlopen(request.url)
            newResponse.status_code = 200
            newResponse.headers = response.headers
            newResponse.raw = response
            newResponse.encoding = "utf-8"
            self.response = response
        finally:
            return newResponse

    def close(self):
        self.response.close()
