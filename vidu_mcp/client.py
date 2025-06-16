"""Vidu API client base class."""
import requests
from typing import Any, Dict
from vidu_mcp.exceptions import ViduAuthError, ViduRequestError


class ViduAPIClient:
    """Base client for making requests to Vidu API."""

    def __init__(self, api_key: str, api_host: str):
        """Initialize the API client.

        Args:
            api_key: The API key for authentication
            api_host: The API host URL
        """
        self.api_key = api_key
        self.api_host = api_host
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token {api_key}',
        })

    def _make_request(
            self,
            method: str,
            endpoint: str,
            **kwargs
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Vidu API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments to pass to requests

        Returns:
            API response data as dictionary

        Raises:
            ViduAuthError: If authentication fails
            ViduRequestError: If the request fails
        """
        url = f"{self.api_host}{endpoint}"

        # Set Content-Type based on whether files are being uploaded
        files = kwargs.get('files')
        if not files:
            self.session.headers['Content-Type'] = 'application/json'
        else:
            # Remove Content-Type header for multipart/form-data
            # requests library will set it automatically with the correct boundary
            self.session.headers.pop('Content-Type', None)

        try:
            response = self.session.request(method, url, **kwargs)

            # Check for other HTTP errors
            response.raise_for_status()

            data = response.json()

            # Check API-specific error codes
            if data.get("code") is not None:
                match data.get("code"):
                    case 401:
                        raise ViduAuthError(
                            f"API Error: {data.get('message')}, please check your API key and API host."
                            f"Trace-Id: {data.get('metadata', {}).get('trace_id')}"
                        )
                    case _:
                        raise ViduRequestError(
                            f"API Error: {data.get('message')}"
                            f"Trace-Id: {data.get('metadata', {}).get('trace_id')}"
                        )

            return data

        except requests.exceptions.RequestException as e:
            raise ViduRequestError(f"Request failed: {str(e)}")

    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a GET request."""
        return self._make_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a POST request."""
        return self._make_request("POST", endpoint, **kwargs)