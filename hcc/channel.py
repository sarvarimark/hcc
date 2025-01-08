"""This module defines the Channel class, which provides methods for making HTTP requests."""
from typing import Callable, Optional, Dict
import requests
from .retry import retry_function, RetryPolicy

class Channel:
    """The Channel class is a helper class for making HTTP requests.

    The Channel class is a wrapper around the requests library.
    It also implements retry functionalities for retrying failed requests. A request is considered
    failed if the status code is not in the success_status_codes list (200, 201).

    The Channel class takes the following parameters:
        url: The URL to which the requests will be sent.
        timeout: The timeout for the requests (default is 2.0 seconds).
        max_retry_count: The maximum number of retries for failed requests (default is 5).
                         If set to None, there is no limit on the number of retries.
        retry_policy: The retry policy to be used when retrying the failed requests
                      (default is None).
        base_delay: The base delay to be used when retrying the failed requests in milliseconds
                    (default is None).

    Typical usage example:
    ```python
    from hcc import Channel

    channel = Channel("https://api.example.com")
    response = channel.get()
    print(response.json())
    ```
    """
    def __init__(
        self,
        url: str,
        timeout: float = 2.0,
        max_retry_count: Optional[int] = 5,
        retry_policy: Optional[RetryPolicy] = None,
        base_delay: Optional[int] = None
    ):
        self.url = url
        self.timeout = timeout
        self.max_retry_count = max_retry_count
        self.retry_policy = retry_policy
        self.base_delay = base_delay
        self.success_status_codes = [200, 201]
        self.is_retry_needed : Callable[[requests.Response], bool] = (
            lambda response: response.status_code not in self.success_status_codes
        )

    def get(
        self,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """The get method sends a GET request.

        Args:
            params: The query parameters for the request (default is an empty dictionary).
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response from the first successful or last request.
        """
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        return retry_function(
            func=lambda: requests.get(
                self.url, timeout=self.timeout, params=params, headers=headers
            ),
            is_retry_needed=self.is_retry_needed,
            max_retry_count=self.max_retry_count,
            retry_policy=self.retry_policy,
            base_delay=self.base_delay
        )

    def post(
        self,
        data: Dict[str, str],
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """The post method sends a POST request.

        Args:
            data: The data to be sent in the body of the request (required).
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response from the first successful or last request.
        """
        if headers is None:
            headers = {}
        return retry_function(
            func=lambda: requests.post(
                self.url, timeout=self.timeout, data=data, headers=headers
            ),
            is_retry_needed=self.is_retry_needed,
            max_retry_count=self.max_retry_count,
            retry_policy=self.retry_policy,
            base_delay=self.base_delay
        )

    def put(
        self,
        data: Dict[str, str],
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """The put method sends a PUT request.

        Args:
            data: The data to be sent in the body of the request (required).
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response.
        """
        if headers is None:
            headers = {}
        return retry_function(
            func=lambda: requests.put(
                self.url, timeout=self.timeout, data=data, headers=headers
            ),
            is_retry_needed=self.is_retry_needed,
            max_retry_count=self.max_retry_count,
            retry_policy=self.retry_policy,
            base_delay=self.base_delay
        )

    def delete(self, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """The delete method sends a DELETE request.

        Args:
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response from the first successful or last request.
        """
        if headers is None:
            headers = {}
        return retry_function(
            func=lambda: requests.delete(
                self.url, timeout=self.timeout, headers=headers
            ),
            is_retry_needed=self.is_retry_needed,
            max_retry_count=self.max_retry_count,
            retry_policy=self.retry_policy,
            base_delay=self.base_delay
        )

    def patch(
        self,
        data: Dict[str, str],
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """The patch method sends a PATCH request.

        Args:
            data: The data to be sent in the body of the request (required).
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response from the first successful or last request.
        """
        if headers is None:
            headers = {}
        return retry_function(
            func=lambda: requests.patch(
                self.url, timeout=self.timeout, data=data, headers=headers
            ),
            is_retry_needed=self.is_retry_needed,
            max_retry_count=self.max_retry_count,
            retry_policy=self.retry_policy,
            base_delay=self.base_delay
        )
